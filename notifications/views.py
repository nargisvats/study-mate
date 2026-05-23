from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Notification


@login_required
def notification_list(request):
    notifications = request.user.notifications.all()[:50]
    return render(request, "notifications/list.html", {"notifications": notifications})


@login_required
@require_POST
def mark_read(request, pk):
    n = get_object_or_404(Notification, pk=pk, user=request.user)
    n.is_read = True
    n.save(update_fields=["is_read"])
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        unread = request.user.notifications.filter(is_read=False).count()
        return JsonResponse({"unread": unread})
    return redirect("notifications:list")


@login_required
def unread_count(request):
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({"unread": count})
