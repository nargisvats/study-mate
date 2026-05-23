from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from profiles.models import StudentProfile, TutorProfile
from scheduling.models import Booking


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="review")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="reviews_written")
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review {self.rating}★ for {self.tutor}"
