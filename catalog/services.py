from decimal import Decimal

from django.db.models import Avg, Q

from profiles.models import TutorProfile

from .models import Subject, TutorSubject


class TutorSearchService:
    @staticmethod
    def search(
        subject_id=None,
        country=None,
        language_id=None,
        min_price=None,
        max_price=None,
        min_rating=None,
        min_experience=None,
        offers_free_demo=None,
        query=None,
        sort="rating",
    ):
        qs = TutorProfile.objects.filter(
            verification_status=TutorProfile.VerificationStatus.APPROVED,
            user__status="ACTIVE",
        ).select_related("user").prefetch_related("languages", "tutor_subjects__subject")

        subject_filters = Q()
        if subject_id:
            subject_filters &= Q(tutor_subjects__subject_id=subject_id)
        if min_price is not None:
            subject_filters &= Q(tutor_subjects__hourly_rate__gte=min_price)
        if max_price is not None:
            subject_filters &= Q(tutor_subjects__hourly_rate__lte=max_price)
        if offers_free_demo:
            subject_filters &= Q(tutor_subjects__offers_free_demo=True)
        if subject_filters:
            qs = qs.filter(subject_filters)

        if country:
            qs = qs.filter(country__icontains=country)
        if language_id:
            qs = qs.filter(languages__id=language_id)
        if min_experience is not None:
            qs = qs.filter(years_experience__gte=min_experience)
        if min_rating is not None:
            qs = qs.filter(avg_rating__gte=Decimal(str(min_rating)))
        if query:
            qs = qs.filter(
                Q(display_name__icontains=query)
                | Q(bio__icontains=query)
                | Q(qualification__icontains=query)
            )

        qs = qs.distinct()

        if sort == "price_low":
            qs = qs.annotate(min_rate=Avg("tutor_subjects__hourly_rate")).order_by("min_rate")
        elif sort == "price_high":
            qs = qs.annotate(max_rate=Avg("tutor_subjects__hourly_rate")).order_by("-max_rate")
        elif sort == "experience":
            qs = qs.order_by("-years_experience")
        else:
            qs = qs.order_by("-avg_rating", "-review_count")

        return qs

    @staticmethod
    def get_subjects():
        return Subject.objects.all()
