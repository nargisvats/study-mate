from django.conf import settings
from django.db import models

from scheduling.models import Booking


class SessionRoom(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="session_room")
    provider = models.CharField(max_length=32, default="jitsi")
    external_room_id = models.CharField(max_length=255)
    join_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.external_room_id}"


class SessionFile(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="session_files")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="sessions/")
    original_name = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name or str(self.file)
