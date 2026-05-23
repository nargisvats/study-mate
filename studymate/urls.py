from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from studymate.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("profiles/", include("profiles.urls")),
    path("catalog/", include("catalog.urls")),
    path("scheduling/", include("scheduling.urls")),
    path("payments/", include("payments.urls")),
    path("sessions/", include("sessions_live.urls")),
    path("reviews/", include("reviews.urls")),
    path("notifications/", include("notifications.urls")),
    path("admin-ops/", include("admin_ops.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
