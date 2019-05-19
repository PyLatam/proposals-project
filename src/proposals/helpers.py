from dateutil.parser import parse

from langdetect import detect

from django.db.models import OuterRef, Subquery
from django.db import models
from django.utils import timezone

from .models import Proposal, ProposalAuthor


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


def import_from_json(data):
    keys = ('title', 'abstract', 'description', 'audience_level')

    for raw_proposal in data:
        author = ProposalAuthor.objects.get_or_create(
            name=raw_proposal['name'],
            email=raw_proposal['email'],
        )[0]
        timestamp = parse(raw_proposal['created_at'])

        cleaned_data = {k: raw_proposal[k] for k in keys}

        try:
            proposal = Proposal.objects.get(added_on=timestamp)
        except Proposal.DoesNotExist:
            proposal = Proposal(added_on=timestamp)
        else:
            cleaned_data['timestamp'] = proposal.data['timestamp']

        if proposal.data == cleaned_data:
            continue

        cleaned_data['timestamp'] = timezone.now().strftime('%Y-%m-%dT%H:%M:%S')

        if proposal.pk:
            # Proposal content has changed
            proposal.updated_on = timezone.now()
        proposal.author = author
        proposal.data = cleaned_data
        # Django bug fixed in 2.2.1
        proposal.data_history.append(cleaned_data)
        proposal.language = detect(cleaned_data['abstract'])
        proposal.save()
