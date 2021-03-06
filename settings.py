# -*- coding: utf-8 -*-
from getenv import env
from django.urls import reverse_lazy


INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())

USE_TZ = True
USE_L10N = True
TIME_ZONE = 'America/New_York'

# all django settings can be altered here
ENABLE_SYNCING = False
STATIC_ROOT = '/static'
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
INSTALLED_APPS.extend([
    'core',
    'accounts',
    'proposals',
    'social_django',
])


# Accounts
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication
    'social_core.backends.github.GithubOAuth2',  # for Github authentication
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = 'landing_page'
LOGOUT_REDIRECT_URL = 'landing_page'
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_USER_FIELDS = ['email', 'first_name', 'last_name']
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email']
SOCIAL_AUTH_USER_MODEL = 'accounts.User'
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = False
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('GOOGLE_API_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('GOOGLE_API_CLIENT_SECRET')
SOCIAL_AUTH_GITHUB_KEY = env('GITHUB_API_CLIENT_ID')
SOCIAL_AUTH_GITHUB_SECRET = env('GITHUB_API_CLIENT_SECRET')
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
SOCIAL_AUTH_SANITIZE_REDIRECTS = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL = reverse_lazy(LOGIN_REDIRECT_URL)
SOCIAL_AUTH_SESSION_EXPIRATION = True
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_INACTIVE_USER_LOGIN = False

PROPOSAL_VOTING_CLOSED = env('PROPOSAL_VOTING_OPEN', default=False)

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social_core.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social_core.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social_core.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social_core.pipeline.social_auth.social_user',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    'social_core.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social_core.pipeline.user.create_user',

    # Notify admin on new user for activation
    'accounts.auth_pipelines.notify_admin',

    # Create the record that associates the social account with the user.
    'social_core.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social_core.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social_core.pipeline.user.user_details',
)

# Email
ADMIN_EMAILS = ['vote@pylatam.org']
DEFAULT_FROM_EMAIL = 'PyLatam noreply@pylatam.org'

TALK_LANGUAGES = (
    ('en', 'English'),
    ('es', 'Spanish'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.current_site',
            ],
        },
    },
]
