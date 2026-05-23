from django.conf import settings


def site_settings(request):
    return {
        "SITE_URL": settings.SITE_URL,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
        "LIVE_PROVIDER": settings.LIVE_PROVIDER,
    }
