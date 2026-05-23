from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User
from profiles.models import StudentProfile


class AuthTests(TestCase):
    def test_student_registration(self):
        client = Client()
        resp = client.post(reverse("accounts:register_student"), {
            "username": "newstudent",
            "email": "s@test.com",
            "first_name": "New",
            "last_name": "Student",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username="newstudent", role=User.Role.STUDENT).exists())
        self.assertTrue(StudentProfile.objects.filter(user__username="newstudent").exists())
