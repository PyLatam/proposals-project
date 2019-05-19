import requests

from getenv import env

from django.core.management.base import BaseCommand

from proposals.helpers import import_from_json


class Command(BaseCommand):

    def handle(self, *args, **options):
        token = env('PAPERCALL_TOKEN', required=True)
        download_endpoint = env('PAPERCALL_DOWNLOAD_URL', required=True)
        cookies = {'_the_papercall_session': token}
        response = requests.get(download_endpoint, cookies=cookies)
        import_from_json(response.json())
