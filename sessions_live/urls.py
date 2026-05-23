from django.urls import path

from . import views

app_name = "sessions_live"

urlpatterns = [
    path("room/<int:booking_id>/", views.session_room, name="room"),
]
