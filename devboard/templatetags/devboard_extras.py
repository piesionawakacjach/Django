from django import template

from devboard.badges import render_status_badge

register = template.Library()


@register.filter
def status_badge(task):
    return render_status_badge(task)