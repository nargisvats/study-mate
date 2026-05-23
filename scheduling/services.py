from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone

from catalog.models import TutorSubject
from notifications.services import NotificationService

from .models import AvailabilitySlot, Booking, BookingParticipant


class SchedulingService:
    ACTIVE_STATUSES = [
        Booking.Status.REQUESTED,
        Booking.Status.PENDING_PAYMENT,
        Booking.Status.CONFIRMED,
        Booking.Status.IN_PROGRESS,
    ]

    @staticmethod
    def local_to_utc(dt_local, tz_name):
        try:
            tz = ZoneInfo(tz_name)
        except (ZoneInfoNotFoundError, ValueError, TypeError, KeyError):
            tz = ZoneInfo("UTC")
        if timezone.is_naive(dt_local):
            dt_local = timezone.make_aware(dt_local, tz)
        return dt_local.astimezone(ZoneInfo("UTC"))

    @staticmethod
    def utc_to_local(dt_utc, tz_name):
        try:
            tz = ZoneInfo(tz_name)
        except (ZoneInfoNotFoundError, ValueError, TypeError, KeyError):
            tz = ZoneInfo("UTC")
        return dt_utc.astimezone(tz)

    @classmethod
    def has_conflict(cls, tutor, start_utc, end_utc, exclude_booking_id=None):
        qs = Booking.objects.filter(
            tutor=tutor,
            status__in=cls.ACTIVE_STATUSES,
            start_utc__lt=end_utc,
            end_utc__gt=start_utc,
        )
        if exclude_booking_id:
            qs = qs.exclude(pk=exclude_booking_id)
        return qs.exists()

    @classmethod
    def slot_in_availability(cls, tutor, start_utc, end_utc):
        dow = start_utc.weekday()
        start_t = start_utc.time()
        end_t = end_utc.time()
        return AvailabilitySlot.objects.filter(
            tutor=tutor,
            day_of_week=dow,
            is_active=True,
            start_utc__lte=start_t,
            end_utc__gte=end_t,
        ).exists()

    @classmethod
    def create_booking(cls, student, tutor, tutor_subject, start_utc, end_utc, is_free_demo=False, booking_type="ONE_ON_ONE", max_participants=1):
        if start_utc >= end_utc:
            raise ValidationError("End time must be after start time.")
        if start_utc < timezone.now():
            raise ValidationError("Cannot book in the past.")
        if not tutor.is_verified:
            raise ValidationError("Tutor is not verified.")
        if cls.has_conflict(tutor, start_utc, end_utc):
            raise ValidationError("This time slot conflicts with an existing booking.")
        if not cls.slot_in_availability(tutor, start_utc, end_utc):
            raise ValidationError("Selected time is outside tutor availability.")

        price = 0 if is_free_demo else tutor_subject.hourly_rate
        duration_hours = (end_utc - start_utc).total_seconds() / 3600
        from decimal import Decimal
        total_price = price * Decimal(duration_hours) if not is_free_demo else 0

        status = Booking.Status.REQUESTED
        if is_free_demo and tutor.auto_confirm_bookings:
            status = Booking.Status.CONFIRMED
        elif not is_free_demo:
            status = Booking.Status.PENDING_PAYMENT

        booking = Booking.objects.create(
            student=student,
            tutor=tutor,
            subject=tutor_subject.subject,
            tutor_subject=tutor_subject,
            booking_type=booking_type,
            start_utc=start_utc,
            end_utc=end_utc,
            status=status,
            price_snapshot=total_price,
            currency=tutor_subject.currency,
            is_free_demo=is_free_demo,
            max_participants=max_participants,
        )

        NotificationService.notify_booking_created(booking)
        return booking

    @classmethod
    def confirm_booking(cls, booking):
        booking.status = Booking.Status.CONFIRMED
        booking.save(update_fields=["status", "updated_at"])
        from sessions_live.services import SessionService
        SessionService.ensure_room(booking)
        NotificationService.notify_booking_confirmed(booking)

    @classmethod
    def complete_booking(cls, booking):
        booking.status = Booking.Status.COMPLETED
        booking.save(update_fields=["status", "updated_at"])
        NotificationService.notify_session_completed(booking)

    @classmethod
    def cancel_booking(cls, booking):
        booking.status = Booking.Status.CANCELLED
        booking.save(update_fields=["status", "updated_at"])

    @classmethod
    def join_group_booking(cls, booking, student):
        if booking.booking_type != Booking.BookingType.GROUP:
            raise ValidationError("Not a group booking.")
        if booking.participant_count >= booking.max_participants:
            raise ValidationError("Group session is full.")
        if booking.student_id == student.id:
            raise ValidationError("You are already the primary student.")
        BookingParticipant.objects.get_or_create(booking=booking, student=student)
