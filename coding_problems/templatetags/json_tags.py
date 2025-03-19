from django import template
import json

register = template.Library()

@register.filter
def pretty_json(value):
    if value is None:
        return "None"
    try:
        return json.dumps(value, indent=2)
    except Exception:
        return str(value)