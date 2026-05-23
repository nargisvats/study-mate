from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("student/edit/", views.student_edit, name="student_edit"),
    path("tutor/", views.tutor_dashboard, name="tutor_dashboard"),
    path("tutor/edit/", views.tutor_edit, name="tutor_edit"),
    path("tutor/subject/add/", views.tutor_add_subject, name="tutor_add_subject"),
    path("tutor/credential/add/", views.tutor_add_credential, name="tutor_add_credential"),
    path("tutor/demo/add/", views.tutor_add_demo, name="tutor_add_demo"),
    path("tutor/<int:pk>/", views.tutor_public, name="tutor_public"),
]
