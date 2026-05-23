from django.core.mail import send_mail
from django.conf import settings

from .models import Notification


class NotificationService:
    @staticmethod
    def _create(user, ntype, title, message, link=""):
        return Notification.objects.create(
            user=user,
            notification_type=ntype,
            title=title,
            message=message,
            link=link,
        )

    @staticmethod
    def notify_booking_created(booking):
        NotificationService._create(
            booking.tutor.user,
            Notification.NotificationType.BOOKING,
            "New booking request",
            f"{booking.student} requested a session on {booking.start_utc:%Y-%m-%d %H:%M} UTC.",
            f"/scheduling/bookings/",
        )

    @staticmethod
    def notify_booking_confirmed(booking):
        NotificationService._create(
            booking.student.user,
            Notification.NotificationType.BOOKING,
            "Booking confirmed",
            f"Your session with {booking.tutor} is confirmed.",
            f"/sessions/room/{booking.pk}/",
        )

    @staticmethod
    def notify_session_completed(booking):
        NotificationService._create(
            booking.student.user,
            Notification.NotificationType.BOOKING,
            "Session completed",
            f"Leave a review for {booking.tutor}.",
            f"/reviews/create/{booking.pk}/",
        )

    @staticmethod
    def notify_review_received(review):
        NotificationService._create(
            review.tutor.user,
            Notification.NotificationType.REVIEW,
            "New review",
            f"You received a {review.rating}-star review.",
            f"/profiles/tutor/{review.tutor.pk}/",
        )

    @staticmethod
    def notify_verification_approved(tutor):
        NotificationService._create(
            tutor.user,
            Notification.NotificationType.VERIFICATION,
            "Profile approved",
            "Your tutor profile has been verified. You can now receive bookings.",
        )

    @staticmethod
    def send_session_reminder(booking):
        NotificationService._create(
            booking.student.user,
            Notification.NotificationType.REMINDER,
            "Upcoming session",
            f"Your session with {booking.tutor} starts soon.",
            f"/sessions/room/{booking.pk}/",
        )
        NotificationService._create(
            booking.tutor.user,
            Notification.NotificationType.REMINDER,
            "Upcoming session",
            f"Your session with {booking.student} starts soon.",
            f"/sessions/room/{booking.pk}/",
        )
        if booking.student.user.email:
            send_mail(
                subject="StudyMate: Session reminder",
                message=f"Your session starts at {booking.start_utc}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.student.user.email],
                fail_silently=True,
            )
