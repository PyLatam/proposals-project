# -*- coding: utf-8 -*-
import os
import json
from dateutil.parser import parse

from langdetect import detect

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from proposals.models import Proposal, ProposalAuthor


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--location',
            type=str,
            dest='location',
        )

    def handle(self, *args, **options):
        location = options['location']

        if not location or not os.path.isfile(location):
            raise CommandError(f'{location} is not a valid file')

        keys = ('title', 'abstract', 'description', 'audience_level')

        with open(location, 'rb') as raw_file:
            data = json.load(raw_file)

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

                if proposal.data == cleaned_data:
                    continue

                cleaned_data['timestamp'] = timezone.now().strftime('%Y-%m-%dT%H:%M:%S')

                if proposal.pk:
                    # Proposal content has changed
                    proposal.updated_on = timezone.now()
                proposal.author = author
                proposal.data = cleaned_data
                # Django bug fixed in 2.2.1
                # proposal.data_history.append(cleaned_data)
                proposal.language = detect(cleaned_data['abstract'])
                proposal.save()
