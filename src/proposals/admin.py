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
        'yes_vote_count',
        'no_vote_count',
        'skip_vote_count',
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
        'yes_vote_count',
        'no_vote_count',
        'skip_vote_count',
        'data',
        'data_history',
        'withdrawn',
    ]
    fieldsets = (
        (None, {'fields': ('title', 'author', 'abstract', 'description')}),
        ('Dates', {'fields': ('added_on', 'updated_on')}),
        ('Meta', {'fields': ('language', 'audience_level', 'withdrawn')}),
        ('Votes', {'fields': ('yes_vote_count', 'no_vote_count', 'skip_vote_count')}),
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

    def yes_vote_count(self, obj):
        return obj.y_vote_count
    yes_vote_count.admin_order_field = 'y_vote_count'

    def no_vote_count(self, obj):
        return obj.n_vote_count
    no_vote_count.admin_order_field = 'n_vote_count'

    def skip_vote_count(self, obj):
        return obj.s_vote_count
    skip_vote_count.admin_order_field = 's_vote_count'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProposalInline(admin.TabularInline):
    model = Proposal
