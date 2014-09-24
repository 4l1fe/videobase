# coding: utf-8

from django import template

register = template.Library()


@register.filter(name='dict_get')
def dict_get(map, key):
    if isinstance(map, dict):
        try:
            return map[key]
        except:
            pass

        try:
            return map[str(key)]
        except:
            pass

    else:
        try:
            return getattr(map, key)()
        except:
            pass

        try:
            return getattr(map, key)
        except:
            pass

    return ''
