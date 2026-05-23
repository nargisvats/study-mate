from django.conf import settings
from django.db import models


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        BOOKING = "BOOKING", "Booking"
        PAYMENT = "PAYMENT", "Payment"
        REVIEW = "REVIEW", "Review"
        VERIFICATION = "VERIFICATION", "Verification"
        REMINDER = "REMINDER", "Reminder"
        SYSTEM = "SYSTEM", "System"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
