from django import forms

from .models import SessionFile


class SessionFileForm(forms.ModelForm):
    class Meta:
        model = SessionFile
        fields = ["file"]
