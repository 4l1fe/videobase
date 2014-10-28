from bs4 import BeautifulSoup
from apps.contents.constants import APP_CONTENTS_PRICE_TYPE_FREE
from apps.films.models import Films
from crawler.locations_saver import save_location_to_locs_dict, save_existed_location_to_locs_dict
from crawler.tasks.locrobots_logging import fill_log_table_for_not_schema_corresponded_robots
from crawler.tor import simple_tor_get_page
from crawler.utils.locations_utils import sane_dict, save_location

HOST = 'http://my.mail.ru'


class MailRobot(object):
    def get_film_data(self):

        url = 'http://my.mail.ru/video/catalog/movies'

        content = simple_tor_get_page(url)
        soup = BeautifulSoup(content)
        locations = {
                'info': [],
                'type': 'mail_ru'
        }
        items = soup.findAll('a', {'class': 'link-default'})

        for item in items:
            film_name = item.text
            film_link = item.get('href')
            film_url = HOST + film_link
            film_dict = self.get_film_dict(film_name)

            if not film_dict is None:
                film_dict['type'] = 'mail_ru'
                film_dict['url_view'] = film_url
                film_dict['price'] = 0
                film_dict['price_type'] = APP_CONTENTS_PRICE_TYPE_FREE

                one_loc_res = save_location(**film_dict)
                save_existed_location_to_locs_dict(locations, one_loc_res)
        fill_log_table_for_not_schema_corresponded_robots(locations)
        return locations

    def get_film_dict(self, film_name):
        film_dict = None
        try:
            film = Films.objects.get(name=film_name)
        except Exception:
            return film_dict
        film_dict = sane_dict(film)

        return film_dict
