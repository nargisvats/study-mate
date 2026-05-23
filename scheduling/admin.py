from django.contrib import admin

from .models import AvailabilitySlot, Booking, BookingParticipant


class BookingParticipantInline(admin.TabularInline):
    model = BookingParticipant
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "tutor", "subject", "start_utc", "status", "price_snapshot")
    list_filter = ("status", "booking_type", "is_free_demo")
    inlines = [BookingParticipantInline]


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ("tutor", "day_of_week", "start_utc", "end_utc", "is_active")
