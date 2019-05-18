from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('staging/', views.user_staging, name='staging'),
]
