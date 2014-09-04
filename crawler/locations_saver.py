# coding: utf-8
from apps.contents.models import Locations
from crawler.utils.locations_utils import get_content

__author__ = 'vladimir'


def save_location_to_list(locations_list, film, **film_dict):
    if len(locations_list) == 0:
        pass
    try:
        content = get_content(film, film_dict)
        location = Locations.objects.get(type=film_dict['type'], content=content)
        locations_list.append(location.id)
    except:
        pass