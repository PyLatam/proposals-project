from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.cache import never_cache

from accounts.decorators import active_user_required

from . import helpers
from .helpers import get_proposals_for_list, get_proposals_for_voting
from .models import ProposalVote


@never_cache
@active_user_required
def proposal_view(request, proposal_id):
    proposal = get_object_or_404(
        helpers.get_proposals(request.user),
        pk=proposal_id,
    )

    if request.method == 'POST':
        value = ProposalVote._meta.get_field('decision').to_python(request.POST['vote'])
        proposal.vote(request.user, value)
        messages.success(request, 'Your vote has been saved')
        return redirect('landing_page')
    existing_vote = proposal.votes.filter(voter=request.user).first()
    context = {
        'proposal': proposal,
        'percent': helpers.get_vote_percentage(request.user),
        'votes': proposal.votes.all(),
        'existing_vote': existing_vote,
    }
    return render(request, 'proposals/proposal.html', context)


@active_user_required
def user_votes_view(request):
    context = {
        'percent': helpers.get_vote_percentage(request.user),
        'proposals': get_proposals_for_list(request.user),
    }
    return render(request, 'proposals/user_votes_list.html', context)


@never_cache
@active_user_required
def landing(request):
    if not request.user.languages:
        return redirect('preferences')

    proposal = get_proposals_for_voting(request.user).order_by('?').first()

    if not proposal:
        messages.success(request, "You have voted on every proposal!")
        return redirect('votes_list')
    return redirect('proposal_view', proposal.pk)
