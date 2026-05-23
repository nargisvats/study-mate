from django.urls import path

from . import views

app_name = "scheduling"

urlpatterns = [
    path("availability/", views.availability_list, name="availability_list"),
    path("availability/add/", views.availability_add, name="availability_add"),
    path("bookings/", views.booking_manage, name="booking_manage"),
    path("bookings/<int:pk>/accept/", views.booking_accept, name="booking_accept"),
    path("bookings/<int:pk>/decline/", views.booking_decline, name="booking_decline"),
    path("bookings/<int:pk>/complete/", views.booking_complete, name="booking_complete"),
    path("book/<int:tutor_id>/subject/<int:subject_id>/", views.book_session, name="book_session"),
    path("bookings/<int:pk>/success/", views.booking_success, name="booking_success"),
    path("group/<int:pk>/join/", views.join_group, name="join_group"),
]
