from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse

from profiles.models import StudentProfile, TutorProfile

from .forms import LoginForm, StudentRegistrationForm, TutorRegistrationForm
from .models import User


class StudyMateLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm


def register_student(request):
    if request.user.is_authenticated:
        return redirect("accounts:post_login_redirect")
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user, display_name=user.get_full_name() or user.username)
            login(request, user)
            messages.success(request, "Welcome to StudyMate!")
            return redirect("profiles:student_edit")
    else:
        form = StudentRegistrationForm()
    return render(request, "accounts/register_student.html", {"form": form})


def register_tutor(request):
    if request.user.is_authenticated:
        return redirect("accounts:post_login_redirect")
    if request.method == "POST":
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            TutorProfile.objects.create(
                user=user,
                display_name=user.get_full_name() or user.username,
                verification_status=TutorProfile.VerificationStatus.PENDING,
            )
            login(request, user)
            messages.success(request, "Account created. Complete your tutor profile for verification.")
            return redirect("profiles:tutor_edit")
    else:
        form = TutorRegistrationForm()
    return render(request, "accounts/register_tutor.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


def post_login_redirect(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("accounts:login")
    if user.is_platform_admin():
        return redirect("admin_ops:dashboard")
    if user.is_tutor():
        return redirect("profiles:tutor_dashboard")
    return redirect("profiles:student_dashboard")
