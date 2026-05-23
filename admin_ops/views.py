from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from payments.models import Payment
from profiles.models import TutorProfile
from scheduling.models import Booking
from reviews.models import Review


@login_required
@role_required("ADMIN")
def dashboard(request):
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    stats = {
        "total_users": request.user.__class__.objects.count(),
        "pending_tutors": TutorProfile.objects.filter(
            verification_status=TutorProfile.VerificationStatus.PENDING
        ).count(),
        "bookings_week": Booking.objects.filter(created_at__gte=week_ago).count(),
        "revenue_week": Payment.objects.filter(
            status=Payment.Status.PAID, created_at__gte=week_ago
        ).aggregate(total=Sum("amount"))["total"] or 0,
        "avg_rating": Review.objects.aggregate(avg=Avg("rating"))["avg"] or 0,
        "open_disputes": Payment.objects.filter(dispute_open=True).count(),
        "completed_sessions": Booking.objects.filter(status=Booking.Status.COMPLETED).count(),
    }
    recent_bookings = Booking.objects.select_related("student", "tutor", "subject").order_by("-created_at")[:10]
    pending_tutors = TutorProfile.objects.filter(
        verification_status=TutorProfile.VerificationStatus.PENDING
    ).select_related("user")[:10]
    return render(request, "admin_ops/dashboard.html", {
        "stats": stats,
        "recent_bookings": recent_bookings,
        "pending_tutors": pending_tutors,
    })


@login_required
@role_required("ADMIN")
@require_POST
def approve_tutor(request, pk):
    tutor = get_object_or_404(TutorProfile, pk=pk)
    if tutor.verification_status != TutorProfile.VerificationStatus.APPROVED:
        tutor.verification_status = TutorProfile.VerificationStatus.APPROVED
        tutor.save(update_fields=["verification_status", "updated_at"])
        messages.success(request, f"Approved {tutor.display_name}.")
    return redirect("admin_ops:dashboard")


@login_required
@role_required("ADMIN")
@require_POST
def reject_tutor(request, pk):
    tutor = get_object_or_404(TutorProfile, pk=pk)
    tutor.verification_status = TutorProfile.VerificationStatus.REJECTED
    tutor.save(update_fields=["verification_status", "updated_at"])
    messages.warning(request, f"Rejected {tutor.display_name}.")
    return redirect("admin_ops:dashboard")
