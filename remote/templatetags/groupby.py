from django import template
from itertools import groupby
from operator import itemgetter

register = template.Library()

@register.filter
def groupby(items, attr):
    grouped = {}
    for item in items:
        key = item.get(attr, "Diğer")
        grouped.setdefault(key, []).append(item)
    return grouped.items()
