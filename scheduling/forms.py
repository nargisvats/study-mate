from django import forms

from .models import AvailabilitySlot, Booking


class AvailabilitySlotForm(forms.ModelForm):
    class Meta:
        model = AvailabilitySlot
        fields = ["day_of_week", "start_utc", "end_utc", "is_active"]
        widgets = {
            "start_utc": forms.TimeInput(attrs={"type": "time"}),
            "end_utc": forms.TimeInput(attrs={"type": "time"}),
        }


class BookingForm(forms.Form):
    tutor_subject_id = forms.IntegerField(widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    duration_minutes = forms.IntegerField(min_value=30, max_value=180, initial=60)
    is_free_demo = forms.BooleanField(required=False)
    booking_type = forms.ChoiceField(choices=Booking.BookingType.choices, initial=Booking.BookingType.ONE_ON_ONE)
    max_participants = forms.IntegerField(min_value=2, max_value=20, initial=5, required=False)
