from django.urls import path

from . import views


urlpatterns = [
    path("", views.landing, name="landing_page"),
    path("votes/", views.votes_view, name="votes_list"),
    path("screening/<uuid:proposal_id>/", views.proposal_view, name="proposal_view"),
    path("screening/<uuid:proposal_id>/vote/", views.proposal_vote, name="proposal_vote"),
]
