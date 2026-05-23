import requests
from django.conf import settings

from .models import SessionRoom


class SessionService:
    @classmethod
    def ensure_room(cls, booking):
        room, created = SessionRoom.objects.get_or_create(
            booking=booking,
            defaults=cls._create_room_data(booking),
        )
        if created and settings.LIVE_PROVIDER == "daily" and settings.DAILY_API_KEY:
            cls._upgrade_to_daily(room, booking)
        return room

    @classmethod
    def _create_room_data(cls, booking):
        room_name = f"studymate_booking_{booking.pk}"
        if settings.LIVE_PROVIDER == "daily" and settings.DAILY_API_KEY:
            return {"provider": "daily", "external_room_id": room_name, "join_url": ""}
        domain = settings.JITSI_DOMAIN
        join_url = f"https://{domain}/{room_name}"
        return {"provider": "jitsi", "external_room_id": room_name, "join_url": join_url}

    @classmethod
    def _upgrade_to_daily(cls, room, booking):
        try:
            resp = requests.post(
                "https://api.daily.co/v1/rooms",
                headers={"Authorization": f"Bearer {settings.DAILY_API_KEY}"},
                json={"name": room.external_room_id, "properties": {"exp": int(booking.end_utc.timestamp()) + 3600}},
                timeout=10,
            )
            if resp.status_code in (200, 201):
                data = resp.json()
                room.provider = "daily"
                room.join_url = data.get("url", room.join_url)
                room.save(update_fields=["provider", "join_url"])
        except requests.RequestException:
            pass

    @classmethod
    def get_embed_url(cls, room):
        if room.provider == "daily" and room.join_url:
            return room.join_url
        domain = settings.JITSI_DOMAIN
        return f"https://{domain}/{room.external_room_id}#config.prejoinPageEnabled=false"
