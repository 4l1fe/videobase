# coding: utf-8
__author__ = 'vladimir'


class RobotsTypeChecker():
    def __init__(self):

        self.locrobots = ['amediateka_ru', 'ayyo_ru', 'drugoe_kino', 'itunes', 'ivi_ru', 'megogo_net', 'mosfilm_ru', 'now_ru', 'oll_tv', 'play_google_com', 'playfamily_dot_ru',
                     'stream_ru', 'tvigle_ru', 'tvzavr_ru', 'tvzor_ru', 'viaplay_ru', 'videomax_org', 'youtube_com', 'zabava_ru', 'zoomby_ru']
        self.datarobots = ['kinopoisk_ru', 'youtube_com']
        self.supportrobots = ['location_saver', 'thor', 'main_worker']


    def check_robots_type(self, robot_name):

        if robot_name in self.locrobots:
            return 'locrobot'
        if robot_name in self.datarobots:
            return 'datarobot'
        if robot_name in self.supportrobots:
            return 'supportrobot'

    def get_datarobots_list(self):
        return self.datarobots

    def get_locrobots_list(self):
        return self.locrobots

    def get_support_robots(self):
        return self.supportrobots