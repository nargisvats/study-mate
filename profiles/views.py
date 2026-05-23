from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import role_required
from catalog.models import TutorSubject
from scheduling.models import Booking
from .forms import CredentialForm, DemoMediaForm, StudentProfileForm, TutorProfileForm, TutorSubjectForm
from .models import Credential, DemoMedia, StudentProfile, TutorProfile


@login_required
@role_required("STUDENT")
def student_dashboard(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    upcoming = Booking.objects.filter(student=profile).filter(
        status__in=[Booking.Status.CONFIRMED, Booking.Status.IN_PROGRESS, Booking.Status.PENDING_PAYMENT]
    ).order_by("start_utc")[:10]
    past = Booking.objects.filter(student=profile, status=Booking.Status.COMPLETED).order_by("-start_utc")[:5]
    return render(request, "profiles/student_dashboard.html", {
        "profile": profile, "upcoming": upcoming, "past": past,
    })


@login_required
@role_required("STUDENT")
def student_edit(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profiles:student_dashboard")
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, "profiles/student_edit.html", {"form": form, "profile": profile})


@login_required
@role_required("TUTOR")
def tutor_dashboard(request):
    profile = get_object_or_404(TutorProfile, user=request.user)
    upcoming = Booking.objects.filter(tutor=profile).exclude(
        status__in=[Booking.Status.CANCELLED, Booking.Status.COMPLETED]
    ).order_by("start_utc")[:10]
    from payments.models import Payment
    earnings = Payment.objects.filter(
        booking__tutor=profile, status=Payment.Status.PAID
    ).values_list("amount", flat=True)
    total_earnings = sum(earnings, start=0)
    return render(request, "profiles/tutor_dashboard.html", {
        "profile": profile, "upcoming": upcoming, "total_earnings": total_earnings,
    })


@login_required
@role_required("TUTOR")
def tutor_edit(request):
    profile = get_object_or_404(TutorProfile, user=request.user)
    if request.method == "POST":
        form = TutorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profiles:tutor_dashboard")
    else:
        form = TutorProfileForm(instance=profile)
    subjects = profile.tutor_subjects.select_related("subject")
    return render(request, "profiles/tutor_edit.html", {
        "form": form, "profile": profile, "subjects": subjects,
    })


@login_required
@role_required("TUTOR")
def tutor_add_subject(request):
    profile = get_object_or_404(TutorProfile, user=request.user)
    if request.method == "POST":
        form = TutorSubjectForm(request.POST)
        if form.is_valid():
            ts = form.save(commit=False)
            ts.tutor = profile
            ts.save()
            messages.success(request, "Subject added.")
            return redirect("profiles:tutor_edit")
    else:
        form = TutorSubjectForm()
    return render(request, "profiles/tutor_subject_form.html", {"form": form})


@login_required
@role_required("TUTOR")
def tutor_add_credential(request):
    profile = get_object_or_404(TutorProfile, user=request.user)
    if request.method == "POST":
        form = CredentialForm(request.POST, request.FILES)
        if form.is_valid():
            cred = form.save(commit=False)
            cred.tutor = profile
            cred.save()
            messages.success(request, "Credential added.")
            return redirect("profiles:tutor_edit")
    else:
        form = CredentialForm()
    return render(request, "profiles/credential_form.html", {"form": form})


@login_required
@role_required("TUTOR")
def tutor_add_demo(request):
    profile = get_object_or_404(TutorProfile, user=request.user)
    if request.method == "POST":
        form = DemoMediaForm(request.POST, request.FILES)
        if form.is_valid():
            demo = form.save(commit=False)
            demo.tutor = profile
            demo.save()
            messages.success(request, "Demo media added.")
            return redirect("profiles:tutor_edit")
    else:
        form = DemoMediaForm()
    return render(request, "profiles/demo_form.html", {"form": form})


def tutor_public(request, pk):
    tutor = get_object_or_404(
        TutorProfile.objects.select_related("user").prefetch_related(
            "credentials", "demo_media", "tutor_subjects__subject", "languages"
        ),
        pk=pk,
        verification_status=TutorProfile.VerificationStatus.APPROVED,
    )
    from reviews.models import Review
    reviews = Review.objects.filter(tutor=tutor).select_related("student")[:10]
    return render(request, "profiles/tutor_public.html", {
        "tutor": tutor, "reviews": reviews,
    })
