from django.conf import settings
from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    display_name = models.CharField(max_length=120)
    country = models.CharField(max_length=64, blank=True)
    timezone = models.CharField(max_length=64, default="UTC")
    bio = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    languages = models.ManyToManyField(Language, blank=True, related_name="students")
    avatar = models.ImageField(upload_to="avatars/students/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name


class TutorProfile(models.Model):
    class VerificationStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tutor_profile")
    display_name = models.CharField(max_length=120)
    country = models.CharField(max_length=64, blank=True)
    timezone = models.CharField(max_length=64, default="UTC")
    bio = models.TextField(blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    qualification = models.CharField(max_length=255, blank=True)
    languages = models.ManyToManyField(Language, blank=True, related_name="tutors")
    avatar = models.ImageField(upload_to="avatars/tutors/", blank=True, null=True)
    verification_status = models.CharField(
        max_length=10, choices=VerificationStatus.choices, default=VerificationStatus.PENDING
    )
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.PositiveIntegerField(default=0)
    auto_confirm_bookings = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name

    @property
    def is_verified(self):
        return self.verification_status == self.VerificationStatus.APPROVED


class Credential(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name="credentials")
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    document = models.FileField(upload_to="credentials/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.tutor})"


class DemoMedia(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name="demo_media")
    title = models.CharField(max_length=120, blank=True)
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to="demos/", blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title or f"Demo {self.id}"
