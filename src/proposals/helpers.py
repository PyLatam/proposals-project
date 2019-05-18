from django.db.models import OuterRef, Subquery
from django.db import models

from .models import Proposal


def get_votes_for_user(user):
    updated_proposal = Proposal.objects.filter(
        pk=models.OuterRef('proposal'),
        updated_on__gt=models.OuterRef('updated_on'),
    )
    return user.votes.annotate(outdated=models.Exists(updated_proposal))


def get_vote_percentage(user):
    total = get_proposals(user).count()
    votes = user.votes.count()
    return "%0.2f" % (100.0 * votes/total)

def get_outdated_proposals(user):
    votes = user.votes.filter(proposal=OuterRef('pk')).values('updated_on')
    return get_proposals(user).filter(updated_on__gt=Subquery(votes))


def get_proposals(user):
    return Proposal.objects.active().exclude(author__email__iexact=user.email)


def get_proposals_for_voting(user):
    return get_proposals(user).exclude(votes__voter=user)
