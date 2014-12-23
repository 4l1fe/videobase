# coding: utf-8
from django import template

register = template.Library()


@register.filter(name="values_by_key")
def values_by_key(value, arg):
    if isinstance(value, dict) and arg in value:
        return [item[arg] for item in value]
    else:
        return value


@register.filter(name="array_format", is_save=True)
def array_format(value, arg):
    try:
        if isinstance(value, dict):
            return [arg.format(**item) for item in value]
        else:
            return [arg.format(item=item) for item in value]
    except Exception as e:
        return value
