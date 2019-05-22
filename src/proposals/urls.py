from django.urls import path

from . import views


urlpatterns = [
    path("", views.landing, name="landing_page"),
    path("votes/", views.user_votes_view, name="votes_list"),
    path("screening/<uuid:proposal_id>/", views.proposal_view, name="proposal_view"),
]
