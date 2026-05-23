from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        TUTOR = "TUTOR", "Tutor"
        ADMIN = "ADMIN", "Admin"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    phone = models.CharField(max_length=20, blank=True)

    def is_student(self):
        return self.role == self.Role.STUDENT

    def is_tutor(self):
        return self.role == self.Role.TUTOR

    def is_platform_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
