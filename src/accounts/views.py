from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView


def login(request):
    return TemplateView.as_view(template_name='accounts/login.html')(request)


def logout(request):
    return LogoutView.as_view(template_name='accounts/logout.html')(request)


@login_required
def user_staging(request):
    if request.user.is_active:
        return redirect(settings.LOGIN_REDIRECT_URL)
    return TemplateView.as_view(template_name='accounts/staging.html')(request)
