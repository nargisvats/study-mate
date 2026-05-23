from django.test import TestCase

from accounts.models import User
from catalog.models import Subject, TutorSubject
from catalog.services import TutorSearchService
from profiles.models import TutorProfile


class TutorSearchTests(TestCase):
    def test_search_verified_tutor(self):
        u = User.objects.create_user("t1", password="x", role=User.Role.TUTOR)
        t = TutorProfile.objects.create(
            user=u, display_name="Tutor A",
            verification_status=TutorProfile.VerificationStatus.APPROVED,
            country="USA",
        )
        s = Subject.objects.create(name="Physics", slug="physics")
        TutorSubject.objects.create(tutor=t, subject=s, hourly_rate=40)
        results = TutorSearchService.search(subject_id=s.id, country="USA")
        self.assertIn(t, list(results))

    def test_search_subject_and_price_same_offering(self):
        u = User.objects.create_user("t2", password="x", role=User.Role.TUTOR)
        t = TutorProfile.objects.create(
            user=u, display_name="Tutor B",
            verification_status=TutorProfile.VerificationStatus.APPROVED,
        )
        cheap = Subject.objects.create(name="Chemistry", slug="chemistry")
        expensive = Subject.objects.create(name="Economics", slug="economics")
        TutorSubject.objects.create(tutor=t, subject=cheap, hourly_rate=20)
        TutorSubject.objects.create(tutor=t, subject=expensive, hourly_rate=80)
        results = list(TutorSearchService.search(subject_id=cheap.id, max_price=30))
        self.assertIn(t, results)
        results = list(TutorSearchService.search(subject_id=expensive.id, max_price=30))
        self.assertNotIn(t, results)
