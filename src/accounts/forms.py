from django import forms
from django.conf import settings


def languages():
    yield ('all', 'All')

    for choice in settings.LANGUAGES:
        yield choice


class UserPreferencesForm(forms.Form):
    language = forms.ChoiceField(label='talk language', choices=languages())
