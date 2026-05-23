from django.contrib import admin

from .models import Credential, DemoMedia, Language, StudentProfile, TutorProfile


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "country", "timezone")
    search_fields = ("display_name", "user__username")


@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "country", "verification_status", "avg_rating", "review_count")
    list_filter = ("verification_status", "country")
    search_fields = ("display_name", "user__username")
    actions = ["approve_tutors", "reject_tutors"]

    @admin.action(description="Approve selected tutors")
    def approve_tutors(self, request, queryset):
        for tutor in queryset:
            if tutor.verification_status != TutorProfile.VerificationStatus.APPROVED:
                tutor.verification_status = TutorProfile.VerificationStatus.APPROVED
                tutor.save(update_fields=["verification_status", "updated_at"])

    @admin.action(description="Reject selected tutors")
    def reject_tutors(self, request, queryset):
        queryset.update(verification_status=TutorProfile.VerificationStatus.REJECTED)


admin.site.register(Credential)
admin.site.register(DemoMedia)
