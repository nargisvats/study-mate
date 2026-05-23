from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import User


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles and not request.user.is_superuser:
                return redirect("home")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
