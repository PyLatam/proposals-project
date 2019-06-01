# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path
from django.urls import include
import social_django.urls
import accounts.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('proposals.urls')),
    path('accounts/', include(accounts.urls)),
    path('accounts/', include(social_django.urls)),
]
