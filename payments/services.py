from django.conf import settings

from .providers import MockPaymentProvider, StripePaymentProvider


def get_payment_provider():
    if settings.PAYMENT_PROVIDER == "stripe" and settings.STRIPE_SECRET_KEY:
        return StripePaymentProvider()
    return MockPaymentProvider()
