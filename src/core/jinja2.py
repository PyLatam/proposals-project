import dateutil.parser

import bleach
import markdown2 as markdown
from jinja2 import Environment
from jinja2 import Markup

from django.contrib.messages.api import get_messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def date_filter(d):
    if not d:
        return ''
    if isinstance(d, str):
        d = dateutil.parser.parse(d)
    return d.strftime('%B %-d, %-I:%M %p')

def set_target(attrs, new=False):
    attrs[(None, 'target')] = '_blank'
    return attrs


def time_to_minutes(d):
    return d.hour * 60 + d.minute


def markdown_filter(s):
    if not s:
        return ''
    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'hr', 'pre']
    raw = bleach.clean(markdown.markdown(s), tags=bleach.ALLOWED_TAGS + tags)
    raw = bleach.linkify(raw, callbacks=[set_target])
    return Markup(raw)


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url_for': reverse,
        'config': {},
        'get_messages': get_messages,
    })
    env.filters['date'] = date_filter
    env.filters['minutes'] = time_to_minutes
    env.filters['markdown'] = markdown_filter
    return env
