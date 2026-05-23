from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("tutor", "student", "rating", "created_at")
    list_filter = ("rating",)
