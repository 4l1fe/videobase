# coding: utf-8
def create_location_result(location_type, location_id, film_id, status, is_new):
    loc_dict = {'location_type': location_type,
                'location_id': location_id,
                'film_id': film_id,
                'status': status,
                'is_new': is_new
                }
    return loc_dict


def save_location_to_locs_dict(locations_dict, status, film, loc_type, location_id, is_new):
    try:
        one_loc_result = create_location_result(loc_type, location_id, film.id, status, is_new)
        locations_dict['info'].append(one_loc_result)
        print "Location dict saved"
    except Exception, e:
        import traceback
        traceback.print_exc()
        print "Locations dict saving failed:", e.message


def save_existed_location_to_locs_dict(locations_dict, existed_location):
    for ex_loc in existed_location['info']:
        locations_dict['info'].append(ex_loc)