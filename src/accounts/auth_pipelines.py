from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string


def notify_admin(strategy, details, backend, *args, **kwargs):
    if kwargs.get('is_new'):
        user = kwargs['user']
        site = Site.objects.get_current()
        content_admin = render_to_string(
            'accounts/email/new_user.txt',
            context={'user': user, 'site': site},
        )
        send_mail(
            subject='New voter signup',
            message=content_admin,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ADMIN_EMAILS,
        )
        content_user = render_to_string(
            'accounts/email/welcome_user.txt',
            context={'user': user, 'site': site},
        )
        send_mail(
            subject='Welcome to the PyCon Latam Voting App',
            message=content_user,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
