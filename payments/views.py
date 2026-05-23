import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from scheduling.models import Booking

from .models import Payment
from .services import get_payment_provider


@login_required
def mock_checkout(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, student__user=request.user)
    if request.method == "POST":
        provider = get_payment_provider()
        provider.mark_paid(booking, gateway_id=f"mock_{booking_id}")
        messages.success(request, "Payment successful (mock).")
        return redirect("profiles:student_dashboard")
    return render(request, "payments/mock_checkout.html", {"booking": booking})


@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, student__user=request.user)
    messages.success(request, "Payment received. Your session is confirmed.")
    return redirect("profiles:student_dashboard")


@login_required
def payment_cancel(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, student__user=request.user)
    from scheduling.services import SchedulingService
    SchedulingService.cancel_booking(booking)
    messages.warning(request, "Payment cancelled.")
    return redirect("profiles:student_dashboard")


@csrf_exempt
@require_POST
def stripe_webhook(request):
    provider = get_payment_provider()
    sig = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        provider.handle_webhook(request.body, sig)
        return HttpResponse(status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
