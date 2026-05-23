from django.urls import path

from . import views

app_name = "admin_ops"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("tutors/<int:pk>/approve/", views.approve_tutor, name="approve_tutor"),
    path("tutors/<int:pk>/reject/", views.reject_tutor, name="reject_tutor"),
]
