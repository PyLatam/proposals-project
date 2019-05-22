import dateutil.parser

import bleach
import markdown2

from django import template
from django.utils.html import mark_safe


register = template.Library()


def set_target(attrs, new=False):
    attrs[(None, 'target')] = '_blank'
    return attrs


@register.filter()
def date_filter(d):
    if not d:
        return ''
    if isinstance(d, str):
        d = dateutil.parser.parse(d)
    return d.strftime('%B %-d, %-I:%M %p')


@register.filter()
def time_to_minutes(d):
    return d.hour * 60 + d.minute


@register.filter()
def markdown(s):
    if not s:
        return ''
    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'hr', 'pre']
    raw = bleach.clean(markdown2.markdown(s), tags=bleach.ALLOWED_TAGS + tags)
    raw = bleach.linkify(raw, callbacks=[set_target])
    return mark_safe(raw)
