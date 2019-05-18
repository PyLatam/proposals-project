from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db import transaction

from core.fields import UUIDPrimaryKey

from .query import ProposalQuerySet


class Proposal(models.Model):
    id = UUIDPrimaryKey()
    added_on = models.DateTimeField()
    updated_on = models.DateTimeField(blank=True, null=True, default=None)
    vote_count = models.PositiveIntegerField(default=0)
    withdrawn = models.BooleanField(default=False)
    author = models.ForeignKey(
        'ProposalAuthor',
        on_delete=models.PROTECT,
        related_name='proposals',
    )
    data = JSONField()
    data_history = ArrayField(base_field=JSONField(), default=list, blank=True)
    language = models.CharField(
        max_length=15,
        blank=True,
        choices=settings.LANGUAGES,
        db_index=True,
    )
    accepted = models.BooleanField(default=False)

    objects = ProposalQuerySet.as_manager()

    class Meta:
        ordering = ('-added_on',)

    def __str__(self):
        return self.title

    @property
    def title(self):
        return self.data['title']

    @property
    def abstract(self):
        return self.data['abstract']

    @property
    def description(self):
        return self.data['description']

    @property
    def audience_level(self):
        return self.data['audience_level']

    @transaction.atomic
    def vote(self, user, decision):
        try:
            vote = self.votes.select_for_update().get(voter=user)
        except ProposalVote.DoesNotExist:
            vote = ProposalVote(voter=user, proposal=self)
        vote.decision = decision
        vote.save()
        return vote


class ProposalAuthor(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()

    class Meta:
        # Papercall allows you to change name per proposal
        # So we can't make email a unique field on its own
        unique_together = ('name', 'email')

    def __str__(self):
        return self.name


class ProposalVote(models.Model):
    NO = 1
    YES = 2
    DECISION_CHOICES = (
        (NO, 'No'),
        (YES, 'Yes'),
    )

    id = UUIDPrimaryKey()
    voter = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='votes',
    )
    proposal = models.ForeignKey(
        to=Proposal,
        on_delete=models.PROTECT,
        related_name='votes',
    )
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    decision = models.PositiveSmallIntegerField(choices=DECISION_CHOICES, db_index=True)

    class Meta:
        unique_together = ('voter', 'proposal')

    def __str__(self):
        return self.voter.email

    @property
    def in_favor(self):
        return self.decision == self.YES
