from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from profiles.models import StudentProfile
from scheduling.models import Booking

from .forms import ReviewForm
from .services import ReviewService


@login_required
@role_required("STUDENT")
def create_review(request, booking_id):
    student = get_object_or_404(StudentProfile, user=request.user)
    booking = get_object_or_404(Booking, pk=booking_id, student=student, status=Booking.Status.COMPLETED)
    if hasattr(booking, "review"):
        messages.info(request, "You already reviewed this session.")
        return redirect("profiles:student_dashboard")
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                ReviewService.create_review(
                    booking, student,
                    form.cleaned_data["rating"],
                    form.cleaned_data.get("comment", ""),
                )
                messages.success(request, "Thank you for your review!")
                return redirect("profiles:student_dashboard")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ReviewForm()
    return render(request, "reviews/create_review.html", {"form": form, "booking": booking})
