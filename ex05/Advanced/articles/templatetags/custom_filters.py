from django import template
from django.utils.timesince import timesince
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
import datetime

register = template.Library()

@register.filter
def truncate_synopsis(value, length=20):
    """Truncate the synopsis to a specified length with ellipsis."""
    if len(value) > length:
        return value[:length] + '...'
    return value

@register.filter
def time_since_publication(date):
    """Return a human-readable time since the article was published."""
    if isinstance(date, str):
        # Parse string date to datetime
        date = parse_datetime(date)
    if isinstance(date, datetime.datetime):
        if not is_aware(date):
            date = make_aware(date)
        return timesince(date) + ' ago'
    return 'Invalid date'
