from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe

from .models import Proposal, ProposalVote
from .query import SQCount


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'added_on',
        'updated_on',
        'vote_counts',
    ]
    list_filter = ['language']
    readonly_fields = [
        'author',
        'title',
        'abstract',
        'description',
        'audience_level',
        'added_on',
        'updated_on',
        'vote_counts',
        'data',
        'data_history',
        'withdrawn',
    ]
    fieldsets = (
        (None, {'fields': ('title', 'author', 'abstract', 'description')}),
        ('Dates', {'fields': ('added_on', 'updated_on')}),
        ('Meta', {'fields': ('language', 'audience_level', 'vote_counts', 'withdrawn')}),
        ('History', {'fields': ('data_history',)}),
    )

    def get_queryset(self, request):
        votes = ProposalVote.objects.filter(proposal=models.OuterRef('pk'))
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            y_vote_count=SQCount(votes.filter(decision=ProposalVote.YES)),
            n_vote_count=SQCount(votes.filter(decision=ProposalVote.NO)),
            s_vote_count=SQCount(votes.filter(decision=ProposalVote.SKIP)),
        )
        return queryset

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def vote_counts(self, obj):
        bits = '\n'.join([
            f'<li>Y: {obj.y_vote_count}</li>',
            f'<li>N: {obj.n_vote_count}</li>',
            f'<li>S: {obj.s_vote_count}</li>',
        ])
        return mark_safe(f'<ul>{bits}</ul>')


class ProposalInline(admin.TabularInline):
    model = Proposal
