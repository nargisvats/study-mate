from django.core.paginator import Paginator
from django.shortcuts import render

from profiles.models import Language

from .models import Subject
from .services import TutorSearchService


def tutor_search(request):
    subject_id = request.GET.get("subject") or None
    country = request.GET.get("country", "").strip()
    language_id = request.GET.get("language") or None
    min_price = request.GET.get("min_price") or None
    max_price = request.GET.get("max_price") or None
    min_rating = request.GET.get("min_rating") or None
    min_experience = request.GET.get("min_experience") or None
    offers_free_demo = request.GET.get("free_demo") == "1"
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "rating")

    tutors = TutorSearchService.search(
        subject_id=subject_id,
        country=country or None,
        language_id=language_id,
        min_price=float(min_price) if min_price else None,
        max_price=float(max_price) if max_price else None,
        min_rating=float(min_rating) if min_rating else None,
        min_experience=int(min_experience) if min_experience else None,
        offers_free_demo=offers_free_demo or None,
        query=query or None,
        sort=sort,
    )

    paginator = Paginator(tutors, 12)
    page = paginator.get_page(request.GET.get("page"))

    return render(request, "catalog/tutor_search.html", {
        "tutors": page,
        "subjects": TutorSearchService.get_subjects(),
        "languages": Language.objects.all(),
        "filters": request.GET,
    })
