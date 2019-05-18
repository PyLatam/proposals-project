from django.db import models


class ProposalQuerySet(models.QuerySet):

    def active(self):
        return self.exclude(withdrawn=True)
