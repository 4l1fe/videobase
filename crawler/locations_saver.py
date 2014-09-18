# coding: utf-8
from apps.contents.models import Locations
from crawler.robot_result import create_location_result
from crawler.utils.locations_utils import get_content


def save_location_to_locs_dict(locations_dict, status, **film_dict):
    try:
        film = film_dict['film']
        content = get_content(film, film_dict)
        location = Locations.objects.get(type=film_dict['type'], content=content)
        one_loc_result = create_location_result(film_dict['type'], location.id, film.id, status)
        locations_dict['info'].append(one_loc_result)
        print "locations dict", locations_dict
    except Exception, e:
        print "locations dict saving failed:", e.message
