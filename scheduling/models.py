from django.db import models

from catalog.models import Subject, TutorSubject
from profiles.models import StudentProfile, TutorProfile


class AvailabilitySlot(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name="availability_slots")
    day_of_week = models.PositiveSmallIntegerField(choices=Weekday.choices)
    start_utc = models.TimeField()
    end_utc = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["day_of_week", "start_utc"]

    def __str__(self):
        return f"{self.tutor} day {self.day_of_week} {self.start_utc}-{self.end_utc}"


class Booking(models.Model):
    class BookingType(models.TextChoices):
        ONE_ON_ONE = "ONE_ON_ONE", "1-on-1"
        GROUP = "GROUP", "Group"

    class Status(models.TextChoices):
        REQUESTED = "REQUESTED", "Requested"
        PENDING_PAYMENT = "PENDING_PAYMENT", "Pending Payment"
        CONFIRMED = "CONFIRMED", "Confirmed"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
        DISPUTED = "DISPUTED", "Disputed"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="bookings")
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name="bookings")
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="bookings")
    tutor_subject = models.ForeignKey(TutorSubject, on_delete=models.SET_NULL, null=True, blank=True)
    booking_type = models.CharField(max_length=12, choices=BookingType.choices, default=BookingType.ONE_ON_ONE)
    start_utc = models.DateTimeField()
    end_utc = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="INR")
    is_free_demo = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_utc"]

    def __str__(self):
        return f"Booking {self.id}: {self.student} with {self.tutor}"

    @property
    def participant_count(self):
        return self.participants.count() + 1


class BookingParticipant(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="participants")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="group_bookings")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("booking", "student")
