from bs4 import BeautifulSoup
from apps.contents.constants import APP_CONTENTS_PRICE_TYPE_PAY
from apps.films.models import Films
from crawler.locations_robot_corrector import LocationRobotsCorrector
from crawler.locations_saver import save_location_to_locs_dict
from crawler.tasks.locrobots_logging import fill_log_table_for_not_schema_corresponded_robots
from crawler.tasks.test_robots_ban import MultiLocationRobotsBunCheck
from crawler.tor import simple_tor_get_page
from crawler.utils.locations_utils import sane_dict, save_location


class ItunesRobot(object):

    def get_film_list(self):
        list_film_link = []
        url = 'http://www.apple.com/ru/itunes/charts/movies/'

        content = simple_tor_get_page(url)
        soup = BeautifulSoup(content)

        tags_li = soup.find('section', {'class': 'section movies grid'}).findAll('li')

        for li in tags_li:
            list_film_link.append(li.a.get('href'))

        return list_film_link

    def get_film_data(self):
        locations = {
                'info': [],
                'type': 'itunes'
        }
        list_film_link = self.get_film_list()
        for link in list_film_link:
            content = simple_tor_get_page(link)
            film_name, film_price, price_type = self.parse_film_page(content)
            film_dict = self.get_film_dict(film_name)

            if not film_dict is None:
                film_dict['type'] = 'itunes'
                film_dict['url_view'] = link
                film_dict['price'] = film_price
                film_dict['price_type'] = price_type
                save_location(**film_dict)
                save_location_to_locs_dict(locations, True, **film_dict)
        fill_log_table_for_not_schema_corresponded_robots(locations)
        robot_is_banned = MultiLocationRobotsBunCheck.is_result_looks_like_robot_banned(locations)
        if not robot_is_banned:
            LocationRobotsCorrector.correct_locations(locations, 'itunes')
        return locations

    def parse_film_page(self, content):
        soup = BeautifulSoup(content)
        film_name = soup.find('h1').text
        price_text = soup.find('span', {'class': 'price'}).text.split()
        film_price = float(price_text[0])
        price_type = APP_CONTENTS_PRICE_TYPE_PAY
        return film_name, film_price, price_type

    def get_film_dict(self, film_name):
        film_dict = None
        try:
            film = Films.objects.get(name=film_name)
        except Exception:
            return film_dict
        film_dict = sane_dict(film)

        return film_dict




