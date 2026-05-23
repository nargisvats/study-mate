from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "amount", "currency", "status", "gateway", "dispute_open")
    list_filter = ("status", "gateway", "dispute_open")
    actions = ["open_dispute", "close_dispute"]

    @admin.action(description="Open dispute")
    def open_dispute(self, request, queryset):
        queryset.update(dispute_open=True)

    @admin.action(description="Close dispute")
    def close_dispute(self, request, queryset):
        queryset.update(dispute_open=False)
