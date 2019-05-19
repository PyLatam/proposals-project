import os
import json

from django.core.management.base import BaseCommand, CommandError

from proposals.helpers import import_from_json


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

        with open(location, 'rb') as raw_file:
            data = json.load(raw_file)
            import_from_json(data)
