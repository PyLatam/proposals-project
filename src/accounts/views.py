from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import UserPreferencesForm
from .decorators import active_user_required


def login(request):
    return TemplateView.as_view(template_name='accounts/login.html')(request)


def logout(request):
    messages.info(request, 'You are logged out. Thanks for voting!')
    return LogoutView.as_view()(request)


@active_user_required
def user_preferences(request):
    form = UserPreferencesForm(request.POST or None)

    if form.is_valid():
        request.user.set_language(form.cleaned_data['language'])
        messages.success(request, 'Preferences saved')
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'accounts/preferences.html', {'form': form})
