from datetime import time, timedelta

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from catalog.models import Subject, TutorSubject
from profiles.models import Credential, DemoMedia, Language, StudentProfile, TutorProfile
from reviews.services import ReviewService
from scheduling.models import AvailabilitySlot, Booking
from sessions_live.services import SessionService

DEMO_PASSWORD = "StudyMate123!"


class Command(BaseCommand):
    help = "Seed demo users, tutors, availability, and sample bookings"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing demo usernames before seeding",
        )

    def handle(self, *args, **options):
        call_command("seed_subjects")

        if options["reset"]:
            demo_usernames = [
                "demostudent", "demoadmin", "tutor_alex", "tutor_maya", "tutor_sam",
                "tutor_pending",
            ]
            User.objects.filter(username__in=demo_usernames).delete()

        student_user = self._user(
            "demostudent", User.Role.STUDENT, "demo@student.studymate", "Demo", "Student"
        )
        student, _ = StudentProfile.objects.update_or_create(
            user=student_user,
            defaults={
                "display_name": "Demo Student",
                "country": "USA",
                "timezone": "America/New_York",
                "bio": "Exploring StudyMate for live tutoring.",
            },
        )
        en = Language.objects.filter(code="en").first()
        if en:
            student.languages.set([en])

        admin_user = self._user(
            "demoadmin", User.Role.ADMIN, "admin@studymate.local", "Platform", "Admin"
        )
        admin_user.is_staff = True
        admin_user.save(update_fields=["is_staff"])

        tutors_data = [
            {
                "username": "tutor_alex",
                "display_name": "Alex Rivera",
                "country": "USA",
                "subjects": [("Mathematics", 45, True), ("Physics", 50, False)],
                "years": 8,
                "rating_setup": (4.8, 12),
            },
            {
                "username": "tutor_maya",
                "display_name": "Maya Chen",
                "country": "UK",
                "subjects": [("English", 35, True), ("Spanish", 30, True)],
                "years": 5,
                "rating_setup": (4.5, 6),
            },
            {
                "username": "tutor_sam",
                "display_name": "Sam Okonkwo",
                "country": "Nigeria",
                "subjects": [("Computer Science", 55, False), ("Mathematics", 48, True)],
                "years": 10,
                "rating_setup": (5.0, 3),
            },
        ]

        tutors = []
        for data in tutors_data:
            tutors.append(self._seed_tutor(data, en))

        pending_user = self._user(
            "tutor_pending", User.Role.TUTOR, "pending@studymate.local", "Pending", "Tutor"
        )
        TutorProfile.objects.update_or_create(
            user=pending_user,
            defaults={
                "display_name": "Pending Tutor",
                "country": "Canada",
                "verification_status": TutorProfile.VerificationStatus.PENDING,
                "bio": "Awaiting admin approval.",
            },
        )

        self._seed_bookings(student, tutors[0], tutors[1])

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
        self.stdout.write(f"Password for all demo accounts: {DEMO_PASSWORD}")
        self.stdout.write("Student: demostudent | Admin: demoadmin")
        self.stdout.write("Tutors: tutor_alex, tutor_maya, tutor_sam | Pending: tutor_pending")

    def _user(self, username, role, email, first_name, last_name):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "status": User.Status.ACTIVE,
            },
        )
        if created or not user.has_usable_password():
            user.set_password(DEMO_PASSWORD)
            user.role = role
            user.status = User.Status.ACTIVE
            user.save()
        return user

    def _seed_tutor(self, data, default_language):
        user = self._user(
            data["username"],
            User.Role.TUTOR,
            f"{data['username']}@studymate.local",
            data["display_name"].split()[0],
            data["display_name"].split()[-1],
        )
        tutor, _ = TutorProfile.objects.update_or_create(
            user=user,
            defaults={
                "display_name": data["display_name"],
                "country": data["country"],
                "timezone": "UTC",
                "bio": f"Experienced educator specializing in {data['subjects'][0][0]}.",
                "years_experience": data["years"],
                "qualification": "M.Ed., certified instructor",
                "verification_status": TutorProfile.VerificationStatus.APPROVED,
                "auto_confirm_bookings": True,
            },
        )
        if default_language:
            tutor.languages.set([default_language])

        for day in range(7):
            AvailabilitySlot.objects.update_or_create(
                tutor=tutor,
                day_of_week=day,
                start_utc=time(8, 0),
                defaults={"end_utc": time(22, 0), "is_active": True},
            )

        for subject_name, rate, free_demo in data["subjects"]:
            subject = Subject.objects.get(name=subject_name)
            TutorSubject.objects.update_or_create(
                tutor=tutor,
                subject=subject,
                defaults={
                    "hourly_rate": rate,
                    "currency": "USD",
                    "offers_free_demo": free_demo,
                    "description": f"Personalized {subject_name} lessons.",
                },
            )

        Credential.objects.get_or_create(
            tutor=tutor,
            title="Teaching Certificate",
            defaults={"institution": "StudyMate Academy", "year": 2020},
        )
        DemoMedia.objects.get_or_create(
            tutor=tutor,
            title="Introduction video",
            defaults={"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "sort_order": 0},
        )

        avg_rating, review_count = data["rating_setup"]
        tutor.avg_rating = avg_rating
        tutor.review_count = review_count
        tutor.save(update_fields=["avg_rating", "review_count"])
        return tutor

    def _seed_bookings(self, student, tutor_primary, tutor_secondary):
        math = Subject.objects.get(name="Mathematics")
        ts = TutorSubject.objects.get(tutor=tutor_primary, subject=math)

        now = timezone.now()
        completed_start = (now - timedelta(days=7)).replace(hour=14, minute=0, second=0, microsecond=0)
        completed_end = completed_start + timedelta(hours=1)

        completed, created = Booking.objects.get_or_create(
            student=student,
            tutor=tutor_primary,
            subject=math,
            start_utc=completed_start,
            defaults={
                "tutor_subject": ts,
                "end_utc": completed_end,
                "status": Booking.Status.COMPLETED,
                "price_snapshot": 45,
                "currency": "USD",
                "is_free_demo": False,
            },
        )
        if not hasattr(completed, "review"):
            ReviewService.create_review(completed, student, 5, "Excellent session, very clear explanations.")

        confirmed_start = (now + timedelta(days=2)).replace(hour=15, minute=0, second=0, microsecond=0)
        confirmed_end = confirmed_start + timedelta(hours=1)
        confirmed, _ = Booking.objects.update_or_create(
            student=student,
            tutor=tutor_primary,
            subject=math,
            start_utc=confirmed_start,
            defaults={
                "tutor_subject": ts,
                "end_utc": confirmed_end,
                "status": Booking.Status.CONFIRMED,
                "price_snapshot": 45,
                "currency": "USD",
            },
        )
        SessionService.ensure_room(confirmed)

        english = Subject.objects.get(name="English")
        ts_en = TutorSubject.objects.get(tutor=tutor_secondary, subject=english)
        pending_start = (now + timedelta(days=4)).replace(hour=11, minute=0, second=0, microsecond=0)
        pending_end = pending_start + timedelta(hours=1)
        Booking.objects.update_or_create(
            student=student,
            tutor=tutor_secondary,
            subject=english,
            start_utc=pending_start,
            defaults={
                "tutor_subject": ts_en,
                "end_utc": pending_end,
                "status": Booking.Status.PENDING_PAYMENT,
                "price_snapshot": 35,
                "currency": "USD",
            },
        )

        requested_start = (now + timedelta(days=5)).replace(hour=10, minute=0, second=0, microsecond=0)
        requested_end = requested_start + timedelta(hours=1)
        Booking.objects.update_or_create(
            student=student,
            tutor=tutor_primary,
            subject=math,
            start_utc=requested_start,
            defaults={
                "tutor_subject": ts,
                "end_utc": requested_end,
                "status": Booking.Status.REQUESTED,
                "is_free_demo": True,
                "price_snapshot": 0,
                "currency": "USD",
            },
        )
