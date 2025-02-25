import datetime
from django import template
from django.utils.timezone import now

register = template.Library()

@register.filter
def time_ago(value):
    if not value:
        return ""
    
    diff = now() - value

    if diff.days > 1:
        return f"{diff.days} days ago"
    elif diff.days == 1:
        return "1 day ago"
    elif diff.seconds >= 3600:
        return f"{diff.seconds // 3600} hours ago"
    elif diff.seconds >= 60:
        return f"{diff.seconds // 60} minutes ago"
    else:
        return "Just now"
