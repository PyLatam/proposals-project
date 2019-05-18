# -*- coding: utf-8 -*-
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.urls import include
import social_django.urls
import accounts.urls

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('proposals.urls')),
    path('accounts/', include(accounts.urls)),
    path('accounts/', include(social_django.urls)),
    prefix_default_language=False,
)
