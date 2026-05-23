from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("mock/<int:booking_id>/", views.mock_checkout, name="mock_checkout"),
    path("success/<int:booking_id>/", views.payment_success, name="success"),
    path("cancel/<int:booking_id>/", views.payment_cancel, name="cancel"),
    path("webhook/stripe/", views.stripe_webhook, name="stripe_webhook"),
]
