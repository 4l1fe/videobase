# coding: utf-8
from crawler.robot_result import create_location_result


def save_location_to_locs_dict(locations_dict, status, film, loc_type, location_id):
    try:
        one_loc_result = create_location_result(loc_type, location_id, film.id, status)
        locations_dict['info'].append(one_loc_result)
        print "Location dict saved"
    except Exception, e:
        import traceback
        traceback.print_exc()
        print "Locations dict saving failed:", e.message
