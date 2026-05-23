from abc import ABC, abstractmethod

from django.conf import settings
from django.urls import reverse

from .models import Payment


class PaymentProvider(ABC):
    @abstractmethod
    def create_checkout_session(self, booking, request):
        pass

    @abstractmethod
    def handle_webhook(self, payload, sig_header):
        pass

    def mark_paid(self, booking, gateway_id=""):
        payment, _ = Payment.objects.get_or_create(
            booking=booking,
            defaults={
                "amount": booking.price_snapshot,
                "currency": booking.currency,
                "gateway": settings.PAYMENT_PROVIDER,
            },
        )
        payment.status = Payment.Status.PAID
        payment.gateway_id = gateway_id
        payment.save()
        from scheduling.services import SchedulingService
        SchedulingService.confirm_booking(booking)


class MockPaymentProvider(PaymentProvider):
    def create_checkout_session(self, booking, request):
        return reverse("payments:mock_checkout", kwargs={"booking_id": booking.pk})

    def handle_webhook(self, payload, sig_header):
        return True


class StripePaymentProvider(PaymentProvider):
    def create_checkout_session(self, booking, request):
        import stripe

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": booking.currency.lower(),
                    "product_data": {"name": f"StudyMate: {booking.subject.name}"},
                    "unit_amount": int(booking.price_snapshot * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=request.build_absolute_uri(
                reverse("payments:success", kwargs={"booking_id": booking.pk})
            ),
            cancel_url=request.build_absolute_uri(
                reverse("payments:cancel", kwargs={"booking_id": booking.pk})
            ),
            metadata={"booking_id": str(booking.pk)},
        )
        Payment.objects.update_or_create(
            booking=booking,
            defaults={
                "amount": booking.price_snapshot,
                "currency": booking.currency,
                "gateway": "stripe",
                "gateway_id": session.id,
                "status": Payment.Status.PENDING,
            },
        )
        return session.url

    def handle_webhook(self, payload, sig_header):
        import stripe

        stripe.api_key = settings.STRIPE_SECRET_KEY
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            booking_id = session.get("metadata", {}).get("booking_id")
            if booking_id:
                from scheduling.models import Booking
                booking = Booking.objects.get(pk=booking_id)
                self.mark_paid(booking, session.get("id", ""))
        return True
