from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from accounts.decorators import active_user_required

from . import helpers
from .models import ProposalVote
from .helpers import get_proposals_for_voting


@active_user_required
def proposal_view(request, proposal_id):
    proposal = get_object_or_404(
        helpers.get_proposals(request.user),
        pk=proposal_id,
    )
    existing_vote = proposal.votes.filter(voter=request.user).first()
    context = {
        'proposal': proposal,
        'percent': helpers.get_vote_percentage(request.user),
        'votes': proposal.votes.all(),
        'existing_vote': existing_vote,
    }
    return render(request, 'screening_proposal.html', context)


@require_POST
@active_user_required
def proposal_vote(request, proposal_id):
    value = ProposalVote._meta.get_field('decision').to_python(request.POST['vote'])
    proposal = get_object_or_404(
        helpers.get_proposals(request.user),
        pk=proposal_id,
    )
    existing_vote = proposal.vote(request.user, value)
    context = {
        'votes': proposal.votes.all(),
        'existing_vote': existing_vote,
    }
    return render(request, 'user_vote_snippet.html', context)


@active_user_required
def votes_view(request):
    votes = helpers.get_votes_for_user(request.user)
    context = {
        'percent': helpers.get_vote_percentage(request.user),
        'votes': votes,
    }
    return render(request, 'my_votes.html', context)


@never_cache
@active_user_required
def landing(request):
    proposal = get_proposals_for_voting(request.user).order_by('?').first()

    if not proposal:
        messages.success(request, "You have voted on every proposal!")
        return redirect('votes_list')
    return redirect('proposal_view', proposal.pk)
