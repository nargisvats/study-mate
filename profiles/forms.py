from django import forms

from catalog.models import TutorSubject

from .models import Credential, DemoMedia, StudentProfile, TutorProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["display_name", "country", "timezone", "bio", "goals", "avatar", "languages"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "goals": forms.Textarea(attrs={"rows": 3}),
        }


class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        fields = [
            "display_name", "country", "timezone", "bio", "years_experience",
            "qualification", "avatar", "languages", "auto_confirm_bookings",
        ]
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}


class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = ["title", "institution", "year", "document"]


class DemoMediaForm(forms.ModelForm):
    class Meta:
        model = DemoMedia
        fields = ["title", "video_url", "video_file", "sort_order"]


class TutorSubjectForm(forms.ModelForm):
    class Meta:
        model = TutorSubject
        fields = ["subject", "hourly_rate", "currency", "offers_free_demo", "description"]
