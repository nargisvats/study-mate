from datetime import time, timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from catalog.models import Subject, TutorSubject
from catalog.services import TutorSearchService
from payments.providers import MockPaymentProvider
from profiles.models import StudentProfile, TutorProfile
from reviews.models import Review
from scheduling.models import AvailabilitySlot, Booking
from scheduling.services import SchedulingService
from sessions_live.models import SessionRoom


class SchedulingServiceTests(TestCase):
    def setUp(self):
        student_user = User.objects.create_user("student1", password="pass", role=User.Role.STUDENT)
        tutor_user = User.objects.create_user("tutor1", password="pass", role=User.Role.TUTOR)
        self.student = StudentProfile.objects.create(user=student_user, display_name="Student")
        self.tutor = TutorProfile.objects.create(
            user=tutor_user,
            display_name="Tutor",
            verification_status=TutorProfile.VerificationStatus.APPROVED,
        )
        self.subject = Subject.objects.create(name="Math", slug="math", category="ACADEMIC")
        self.tutor_subject = TutorSubject.objects.create(
            tutor=self.tutor, subject=self.subject, hourly_rate=50, currency="USD"
        )
        start = timezone.now() + timedelta(days=2)
        dow = start.weekday()
        AvailabilitySlot.objects.create(
            tutor=self.tutor,
            day_of_week=dow,
            start_utc=time(0, 0),
            end_utc=time(23, 59),
        )

    def test_create_booking_success(self):
        start = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=2)
        end = start + timedelta(hours=1)
        booking = SchedulingService.create_booking(
            self.student, self.tutor, self.tutor_subject, start, end, is_free_demo=True
        )
        self.assertEqual(booking.status, Booking.Status.CONFIRMED)

    def test_booking_conflict(self):
        start = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=2)
        end = start + timedelta(hours=1)
        SchedulingService.create_booking(
            self.student, self.tutor, self.tutor_subject, start, end, is_free_demo=True
        )
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            SchedulingService.create_booking(
                self.student, self.tutor, self.tutor_subject, start, end, is_free_demo=True
            )


class EndToEndFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student_user = User.objects.create_user(
            "flow_student", password="StudyMate123!", role=User.Role.STUDENT
        )
        self.tutor_user = User.objects.create_user(
            "flow_tutor", password="StudyMate123!", role=User.Role.TUTOR
        )
        self.student = StudentProfile.objects.create(
            user=self.student_user, display_name="Flow Student", timezone="UTC"
        )
        self.tutor = TutorProfile.objects.create(
            user=self.tutor_user,
            display_name="Flow Tutor",
            verification_status=TutorProfile.VerificationStatus.APPROVED,
            country="USA",
        )
        self.subject = Subject.objects.create(name="Biology", slug="biology", category="ACADEMIC")
        self.tutor_subject = TutorSubject.objects.create(
            tutor=self.tutor, subject=self.subject, hourly_rate=40, currency="USD"
        )
        start = timezone.now() + timedelta(days=3)
        AvailabilitySlot.objects.create(
            tutor=self.tutor,
            day_of_week=start.weekday(),
            start_utc=time(0, 0),
            end_utc=time(23, 59),
        )

    def test_tutor_search_and_public_profile(self):
        results = list(TutorSearchService.search(subject_id=self.subject.id, country="USA"))
        self.assertIn(self.tutor, results)
        resp = self.client.get(reverse("profiles:tutor_public", kwargs={"pk": self.tutor.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Book")

    def test_paid_booking_and_mock_payment(self):
        start = timezone.now().replace(hour=12, minute=0, second=0, microsecond=0) + timedelta(days=3)
        end = start + timedelta(hours=1)
        booking = SchedulingService.create_booking(
            self.student, self.tutor, self.tutor_subject, start, end, is_free_demo=False
        )
        self.assertEqual(booking.status, Booking.Status.PENDING_PAYMENT)
        MockPaymentProvider().mark_paid(booking, gateway_id="test")
        booking.refresh_from_db()
        self.assertEqual(booking.status, Booking.Status.CONFIRMED)
        self.assertTrue(SessionRoom.objects.filter(booking=booking).exists())

    def test_completed_session_review_updates_rating(self):
        start = timezone.now() - timedelta(days=1)
        end = start + timedelta(hours=1)
        booking = Booking.objects.create(
            student=self.student,
            tutor=self.tutor,
            subject=self.subject,
            tutor_subject=self.tutor_subject,
            start_utc=start,
            end_utc=end,
            status=Booking.Status.COMPLETED,
            price_snapshot=40,
        )
        self.client.login(username="flow_student", password="StudyMate123!")
        resp = self.client.post(
            reverse("reviews:create", kwargs={"booking_id": booking.pk}),
            {"rating": 4, "comment": "Great tutor"},
        )
        self.assertEqual(resp.status_code, 302)
        self.tutor.refresh_from_db()
        self.assertEqual(self.tutor.review_count, 1)
        self.assertEqual(float(self.tutor.avg_rating), 4.0)
        self.assertTrue(Review.objects.filter(booking=booking).exists())
