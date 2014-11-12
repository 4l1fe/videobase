# coding: utf-8
import json
from apps.films.constants import APP_FILM_SERIAL
from crawler.locations_robot_corrector import LocationRobotsCorrector
from crawler.locations_saver import save_location_to_locs_dict, save_existed_location_to_locs_dict
from crawler.tasks.locrobots_logging import fill_log_table_for_not_schema_corresponded_robots
from crawler.tasks.test_robots_ban import MultiLocationRobotsBunCheck
from utils.common import url_with_querystring
from apps.films.models import Films
from crawler.utils.locations_utils import save_location, sane_dict
from crawler.tor import simple_tor_get_page
from apps.contents.constants import *
import string
import re
from bs4 import BeautifulSoup

HOST = 'www.megogo.net/ru'
URL_SEARCH = 'searchhint'


class MegogoRobot(object):
    def __init__(self, film_id):
        self.film = Films.objects.get(id=film_id)
        self.search_url = URL_SEARCH
        self.params = {'lang': 'ru', 'q': re.sub('[' + string.punctuation + ']', '', self.film.name).lower().strip()}
        url = "http://%s/%s" % (HOST, self.search_url, )
        url = url_with_querystring(url, **self.params)
        self.response = simple_tor_get_page(url)
        self.type = 'megogo'

    def get_data(self):
        locations = {
        'info': [],
        'type': 'megogo'
                }
        try:
            films = json.loads(self.response)['result']
            film_link = None
            serial_list = []
            if self.film.type == APP_FILM_SERIAL:
                regFilmname = re.compile(u'(?P<season>\(\d+ сезон\))')
                for film in films:
                    if film['type'] != 'SERIAL':
                        continue
                    season = regFilmname.search(film['title']).group('season')
                    name = film['title']
                    if season:
                        name = name.replace(season, '')
                        season = int(re.search(ur'\d+', season).group())
                    else:
                        season = 1
                    if name.lower().strip().encode('utf-8').translate(None, string.punctuation) == self.film.name.lower().strip().encode('utf-8').translate(None, string.punctuation):
                        serial_list.append({'season': season, 'season_url': film['view_link']})
                        film_link = film['view_link']
                for season in serial_list:
                    ep_info_list = []
                    season_page = simple_tor_get_page(season['season_url'])
                    season_soup = BeautifulSoup(season_page)
                    episode_list = season_soup.find_all('li', {'class': 'voi episode_item'})
                    for episode in episode_list:
                        ep_tag = episode.find('p', {'class': 'voi__title'})
                        episode_url = ep_tag.a.get('href')
                        episode_num = int(re.search(ur'\d+', ep_tag.a.text).group())
                        ep_info_list.append({'number': episode_num, 'url': episode_url})
                    season['episode_list'] = ep_info_list
            else:
                for film in films:
                    if film['title'].lower().strip().encode('utf-8').translate(None, string.punctuation) == self.film.name.lower().strip().encode('utf-8').translate(None, string.punctuation) and str(self.film.release_date.year) in film['sub_title']:
                        film_link = film
                        break

            price, price_type = self.get_price(film_link)
            if serial_list:
                film_link = serial_list
            resp_list = self.film_dict(self.film, film_link, price, price_type)
            for item in resp_list:
                one_loc_res = save_location(**item)
                save_existed_location_to_locs_dict(locations, one_loc_res)
        except Exception, e:
            print e.message
        fill_log_table_for_not_schema_corresponded_robots(locations)
        robot_is_banned = MultiLocationRobotsBunCheck.is_result_looks_like_robot_banned(locations)
        if not robot_is_banned:
            LocationRobotsCorrector.correct_locations(locations, self.type)
        return locations

    def film_dict(self, film, films_list, price, price_type):
        resp_list = []

        if film.type == APP_FILM_SERIAL:
                for serial_season in films_list:
                    resp_dict = sane_dict(film)
                    resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON
                    resp_dict['type'] = self.type
                    resp_dict['number'] = serial_season['season']
                    resp_dict['value'] = None
                    resp_dict['url_view'] = serial_season['season_url']
                    resp_dict['price'] = price
                    resp_dict['episode'] = 0
                    resp_list.append(resp_dict)
                    for episode in serial_season['episode_list']:
                        resp_dict = sane_dict(film)
                        resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE
                        resp_dict['type'] = self.type
                        resp_dict['number'] = serial_season['season']
                        resp_dict['value'] = None
                        resp_dict['url_view'] = episode['url']
                        resp_dict['price'] = price
                        resp_dict['episode'] = episode['number']
                        resp_list.append(resp_dict)
        else:
            resp_dict = sane_dict(film)
            resp_dict['type'] = self.type
            resp_dict['number'] = 0
            resp_dict['value'] = None
            resp_dict['url_view'] = films_list
            resp_dict['price'] = price
            resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM
            resp_dict['episode'] = 0
            resp_list.append(resp_dict)
        return resp_list

    def get_price(self, film_url, **kwargs):
        price = 0
        price_type = APP_CONTENTS_PRICE_TYPE_FREE
        soup = BeautifulSoup(simple_tor_get_page(film_url))
        rootDiv = soup.find('div', {'class': 'view-wide'})
        aPrice = rootDiv.find('a', {'id': 'btn btn_color'})
        if aPrice != None:
            price_type = APP_CONTENTS_PRICE_TYPE_PAY
            reg = re.search(ur'\d+', aPrice.text)
            price = float(reg.group())
        else:
            aPrice = rootDiv.find('a', {'id': 'paymentSubscribeLink'})
            if aPrice != None:
                price_type = APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION
        return price, price_type