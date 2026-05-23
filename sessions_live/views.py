from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from scheduling.models import Booking

from .forms import SessionFileForm
from .models import SessionFile
from .services import SessionService


def _user_can_access(request, booking):
    user = request.user
    if not user.is_authenticated:
        return False
    if hasattr(user, "student_profile") and booking.student_id == user.student_profile.id:
        return True
    if hasattr(user, "tutor_profile") and booking.tutor_id == user.tutor_profile.id:
        return True
    if user.is_platform_admin():
        return True
    return booking.participants.filter(student__user=user).exists()


@login_required
def session_room(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if not _user_can_access(request, booking):
        messages.error(request, "Access denied.")
        return redirect("home")
    if booking.status not in (Booking.Status.CONFIRMED, Booking.Status.IN_PROGRESS, Booking.Status.COMPLETED):
        messages.warning(request, "Session is not available yet.")
        return redirect("home")
    room = SessionService.ensure_room(booking)
    if booking.status == Booking.Status.CONFIRMED:
        booking.status = Booking.Status.IN_PROGRESS
        booking.save(update_fields=["status", "updated_at"])
    embed_url = SessionService.get_embed_url(room)
    files = booking.session_files.select_related("uploaded_by").order_by("-uploaded_at")
    file_form = SessionFileForm()
    if request.method == "POST" and "upload" in request.POST:
        file_form = SessionFileForm(request.POST, request.FILES)
        if file_form.is_valid():
            sf = file_form.save(commit=False)
            sf.booking = booking
            sf.uploaded_by = request.user
            sf.original_name = request.FILES["file"].name
            sf.save()
            messages.success(request, "File uploaded.")
            return redirect("sessions_live:room", booking_id=booking_id)
    return render(request, "sessions_live/room.html", {
        "booking": booking,
        "room": room,
        "embed_url": embed_url,
        "files": files,
        "file_form": file_form,
    })
