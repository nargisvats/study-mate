from django.contrib import admin

from .models import Subject, TutorSubject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TutorSubject)
class TutorSubjectAdmin(admin.ModelAdmin):
    list_display = ("tutor", "subject", "hourly_rate", "currency", "offers_free_demo")
    list_filter = ("currency", "offers_free_demo")
