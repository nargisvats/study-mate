from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.StudyMateLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/student/", views.register_student, name="register_student"),
    path("register/tutor/", views.register_tutor, name="register_tutor"),
    path("redirect/", views.post_login_redirect, name="post_login_redirect"),
]
