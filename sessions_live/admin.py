from django.contrib import admin

from .models import SessionFile, SessionRoom


@admin.register(SessionRoom)
class SessionRoomAdmin(admin.ModelAdmin):
    list_display = ("booking", "provider", "external_room_id", "created_at")


@admin.register(SessionFile)
class SessionFileAdmin(admin.ModelAdmin):
    list_display = ("booking", "uploaded_by", "original_name", "uploaded_at")
