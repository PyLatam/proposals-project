from functools import wraps

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


def active_user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_active:
                return view_func(request, *args, **kwargs)
            return redirect(settings.SOCIAL_AUTH_INACTIVE_USER_URL)
        path = request.get_full_path()
        return redirect_to_login(path)
    return _wrapped_view
