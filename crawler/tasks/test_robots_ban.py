# coding: utf-8
from ipdb import set_trace
from apps.contents.models import Locations, Contents
from apps.robots.models import Robots
from crawler.core.exceptions import NoSuchFilm
from crawler.locrobots.process_film_from_site import get_html_json_for_file_name
from crawler.locrobots.process_films_tasks import process_one_film, load_and_save_film_page_from_site
from crawler.tasks.locrobots_logging import send_message_for_all_recipients


__author__ = 'vladimir'


class TestRobotsBan():
    def __init__(self):
        pass

    @staticmethod
    def test_all_locrobots():
        for robot in Robots.objects.all():
            TestRobotsBan.test_individual_locrobot(robot.name)

    @staticmethod
    def test_individual_locrobot(robot_name):
        loc_type = TestRobotsBan.get_correct_location_type(robot_name)
        films = TestRobotsBan.get_5_films_for_location_type(loc_type)
        checks = 0
        failed_films = []
        for film in films:
            try:
                ret_locations_dict = TestRobotsBan.process_film_on_site(robot_name, film.id)
                if TestRobotsBan.check_is_locations(ret_locations_dict):
                    checks += 1
                else:
                    failed_films += [film.id]
            except NoSuchFilm:
                failed_films += [film.id]

        #print robot_name, "checks: ", checks, "and films:", len(films)
        TestRobotsBan.analyze_checks(checks, robot_name, failed_films, films)

    @staticmethod
    def get_correct_location_type(robot_name):
        if robot_name != 'ivi_ru':
            loc_type = robot_name.replace('_', '')
        else:
            loc_type = 'ivi'
        return loc_type

    @staticmethod
    def analyze_checks(checks, robot_name, failed_films, films):
        if checks<3 and checks >=1:
            TestRobotsBan.send_warning_message(robot_name, failed_films)
        if checks == 0 and len(films) >0:
            TestRobotsBan.send_ban_message(robot_name)

    @staticmethod
    def get_5_films_for_location_type(location_type):
        locations = Locations.objects.filter(type=location_type)
        i = 0
        films = []
        for location in locations.all():
            if i == 5:
                break
            film = Contents.objects.get(id=location.content.id).film
            films = films + [film]
            i += 1
        return films

    @staticmethod
    def send_warning_message(robot_name, failed_films):
        str_for_send = "Robot {} can't get locations for {}".format(robot_name, failed_films)
        print  '###' + str_for_send
        send_message_for_all_recipients(str_for_send, "robots warning information")

    @staticmethod
    def send_ban_message(robot_name):
        str_for_send = "Robot {} was banned".format(robot_name)
        print  '###' + str_for_send
        send_message_for_all_recipients(str_for_send, "robots ban information")

    @staticmethod
    def process_film_on_site(site, film_id):
        html_file_name = load_and_save_film_page_from_site(site, film_id)
        html_json = get_html_json_for_file_name(html_file_name)
        return process_one_film(site, film_id, html_json)


    @staticmethod
    def check_is_locations(locatios_dict):
        if len(locatios_dict['info']) > 0:
            return True
        return False
