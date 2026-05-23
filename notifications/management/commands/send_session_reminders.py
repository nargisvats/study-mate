from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from scheduling.models import Booking
from notifications.services import NotificationService


class Command(BaseCommand):
    help = "Send reminders for sessions starting in the next hour"

    def handle(self, *args, **options):
        now = timezone.now()
        window_end = now + timedelta(hours=1)
        bookings = Booking.objects.filter(
            status=Booking.Status.CONFIRMED,
            start_utc__gte=now,
            start_utc__lte=window_end,
        )
        count = 0
        for booking in bookings:
            NotificationService.send_session_reminder(booking)
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Sent {count} reminders"))
