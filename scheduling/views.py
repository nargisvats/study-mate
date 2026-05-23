from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import role_required
from catalog.models import TutorSubject
from profiles.models import StudentProfile, TutorProfile
from payments.services import get_payment_provider

from .forms import AvailabilitySlotForm, BookingForm
from .models import AvailabilitySlot, Booking
from .services import SchedulingService


@login_required
@role_required("TUTOR")
def availability_list(request):
    profile = get_object_or_404(TutorProfile, user=request.user)
    slots = profile.availability_slots.all()
    return render(request, "scheduling/availability_list.html", {"slots": slots, "profile": profile})


@login_required
@role_required("TUTOR")
def availability_add(request):
    profile = get_object_or_404(TutorProfile, user=request.user)
    if request.method == "POST":
        form = AvailabilitySlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.tutor = profile
            slot.save()
            messages.success(request, "Availability slot added.")
            return redirect("scheduling:availability_list")
    else:
        form = AvailabilitySlotForm()
    return render(request, "scheduling/availability_form.html", {"form": form})


@login_required
@role_required("TUTOR")
def booking_manage(request):
    profile = get_object_or_404(TutorProfile, user=request.user)
    bookings = profile.bookings.exclude(status=Booking.Status.CANCELLED).order_by("-start_utc")
    return render(request, "scheduling/tutor_bookings.html", {"bookings": bookings})


@login_required
@role_required("TUTOR")
def booking_accept(request, pk):
    profile = get_object_or_404(TutorProfile, user=request.user)
    booking = get_object_or_404(Booking, pk=pk, tutor=profile)
    if booking.status == Booking.Status.REQUESTED:
        SchedulingService.confirm_booking(booking)
        messages.success(request, "Booking confirmed.")
    return redirect("scheduling:booking_manage")


@login_required
@role_required("TUTOR")
def booking_decline(request, pk):
    profile = get_object_or_404(TutorProfile, user=request.user)
    booking = get_object_or_404(Booking, pk=pk, tutor=profile)
    if booking.status == Booking.Status.REQUESTED:
        SchedulingService.cancel_booking(booking)
        messages.info(request, "Booking declined.")
    return redirect("scheduling:booking_manage")


@login_required
@role_required("TUTOR")
def booking_complete(request, pk):
    profile = get_object_or_404(TutorProfile, user=request.user)
    booking = get_object_or_404(Booking, pk=pk, tutor=profile)
    SchedulingService.complete_booking(booking)
    messages.success(request, "Session marked complete.")
    return redirect("scheduling:booking_manage")


@login_required
@role_required("STUDENT")
def book_session(request, tutor_id, subject_id):
    student = get_object_or_404(StudentProfile, user=request.user)
    tutor = get_object_or_404(TutorProfile, pk=tutor_id, verification_status=TutorProfile.VerificationStatus.APPROVED)
    tutor_subject = get_object_or_404(TutorSubject, tutor=tutor, subject_id=subject_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            start_time = form.cleaned_data["start_time"]
            duration = form.cleaned_data["duration_minutes"]
            try:
                tz = ZoneInfo(student.timezone)
            except (ZoneInfoNotFoundError, ValueError, TypeError, KeyError):
                tz = ZoneInfo("UTC")
            start_local = datetime.combine(date, start_time, tzinfo=tz)
            end_local = start_local + timedelta(minutes=duration)
            start_utc = SchedulingService.local_to_utc(start_local, student.timezone)
            end_utc = SchedulingService.local_to_utc(end_local, student.timezone)
            is_free_demo = form.cleaned_data.get("is_free_demo") and tutor_subject.offers_free_demo
            try:
                booking = SchedulingService.create_booking(
                    student=student,
                    tutor=tutor,
                    tutor_subject=tutor_subject,
                    start_utc=start_utc,
                    end_utc=end_utc,
                    is_free_demo=is_free_demo,
                    booking_type=form.cleaned_data["booking_type"],
                    max_participants=form.cleaned_data.get("max_participants") or 1,
                )
                if booking.status == Booking.Status.PENDING_PAYMENT:
                    provider = get_payment_provider()
                    checkout_url = provider.create_checkout_session(booking, request)
                    if checkout_url:
                        return redirect(checkout_url)
                if booking.status == Booking.Status.CONFIRMED:
                    from sessions_live.services import SessionService
                    SessionService.ensure_room(booking)
                messages.success(request, "Booking created successfully.")
                return redirect("scheduling:booking_success", pk=booking.pk)
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = BookingForm(initial={"tutor_subject_id": tutor_subject.id})
    return render(request, "scheduling/book_session.html", {
        "form": form, "tutor": tutor, "tutor_subject": tutor_subject,
    })


@login_required
@role_required("STUDENT")
def join_group(request, pk):
    student = get_object_or_404(StudentProfile, user=request.user)
    booking = get_object_or_404(Booking, pk=pk, booking_type=Booking.BookingType.GROUP)
    try:
        SchedulingService.join_group_booking(booking, student)
        messages.success(request, "Joined group session.")
    except ValidationError as e:
        messages.error(request, str(e))
    return redirect("profiles:student_dashboard")


@login_required
@role_required("STUDENT")
def booking_success(request, pk):
    student = get_object_or_404(StudentProfile, user=request.user)
    booking = get_object_or_404(Booking, pk=pk, student=student)
    return render(request, "scheduling/booking_success.html", {"booking": booking})
