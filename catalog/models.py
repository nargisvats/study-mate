from django.db import models

from profiles.models import TutorProfile


class Subject(models.Model):
    class Category(models.TextChoices):
        ACADEMIC = "ACADEMIC", "Academic"
        LANGUAGE = "LANGUAGE", "Language"
        HOBBY = "HOBBY", "Hobby"
        OTHER = "OTHER", "Other"

    name = models.CharField(max_length=120, unique=True)
    category = models.CharField(max_length=10, choices=Category.choices, default=Category.ACADEMIC)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TutorSubject(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name="tutor_subjects")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="tutor_offerings")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="INR")
    offers_free_demo = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("tutor", "subject")

    def __str__(self):
        return f"{self.tutor} - {self.subject}"
