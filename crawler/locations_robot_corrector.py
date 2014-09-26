# coding: utf-8
from apps.contents.models import Locations
from crawler.utils.locations_utils import get_content

__author__ = 'vladimir'


class LocationRobotsCorrector():
    def __init__(self):
        pass

    @staticmethod
    def correct_locations(found_locations_dict, loc_type):
        db_locations = Locations.objects.filter(type=loc_type)
        db_locs_ids_list = LocationRobotsCorrector.get_locs_ids_list(db_locations)
        robot_result_locs_ids_list = LocationRobotsCorrector.get_locs_ids_list_from_robot_result(found_locations_dict['info'])
        removal_candidates = LocationRobotsCorrector.find_candidates_for_removal(db_locs_ids_list, robot_result_locs_ids_list)
        LocationRobotsCorrector.remove_locations(removal_candidates)

    @staticmethod
    def find_candidates_for_removal(db_locs_ids_list, robot_locations_ids):
        removal_candidates = []
        print "db locs", db_locs_ids_list
        print "robor locs", robot_locations_ids
        robot_result_contents_list_for_locs = LocationRobotsCorrector.get_contents_list_from_ids_list(robot_locations_ids)
        for dbloc in db_locs_ids_list:
            db_content = Locations.objects.get(id=dbloc).content
            if db_content not in robot_result_contents_list_for_locs:
                removal_candidates = removal_candidates + [dbloc]
        return removal_candidates

    @staticmethod
    def get_locs_ids_list(locations):
        db_locs_ids = []
        if len(locations) > 0:
            for loc in locations:
                db_locs_ids = db_locs_ids + [loc.id]
        return db_locs_ids

    @staticmethod
    def get_locs_ids_list_from_robot_result(list_of_locs_dics):
        db_locs_ids = []
        if len(list_of_locs_dics) > 0:
            for loc_dict in list_of_locs_dics:
                db_locs_ids = db_locs_ids + [loc_dict['location_id']]
        return db_locs_ids

    @staticmethod
    def get_contents_list_from_ids_list(ids_list):
        contents_list = []
        if len(ids_list) > 0:
            for id in ids_list:
                location = Locations.objects.get(id=id)
                contents_list = contents_list + [location.content]
        return contents_list

    @staticmethod
    def remove_locations(removal_candidates):
        if len(removal_candidates) > 0:
            print "Deleting not actual locations: ", removal_candidates
        else:
            print "All locations are in actual state."
        for loc_id in removal_candidates:
            l = Locations.objects.get(id=loc_id)
            l.delete()


class LocationCorrectorForOneFilmRobots():
    def __init__(self):
        pass

    @staticmethod
    def corrrect_current_location_if_needed(data):
        content = get_content(data['film'], data)
        l_list = Locations.objects.filter(type=data['type'], content=content)

        if len(l_list) > 0:
            print "Deliting not actual locations: ", l_list
            for loc in l_list:
                loc.delete()
        else:
            print "All locations are actual "
            print content
        #Если найдется в базе локейшн с таким типом  и таким контентом то его можно удалить, т.к на сайте его нет
