from django.db import models
from django.db.models import Subquery


class ProposalQuerySet(models.QuerySet):

    def active(self):
        return self.exclude(withdrawn=True)


class SQCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = models.IntegerField()
