# coding: utf-8


# Базовый класс парсера для страници
from apps.contents.constants import APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM, \
    APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE, APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON
from apps.films.constants import APP_FILM_SERIAL


class BaseParse(object):
    def __init__(self, html, film):
        self.html = html
        self.film_type = film.type

    # Стоимость и варианты оплаты (подписка/просмотр/бесплатно)
    def get_price(self, **kwargs):
        raise NotImplementedError()

    # Ссылка на просмотр
    def get_link(self, **kwargs):
        raise NotImplementedError()

    def get_value(self, **kwargs):
        raise NotImplementedError()

    def get_type(self, **kwargs):
        raise NotImplementedError()

    #Роботы, которые парсят сериалы,
    #должны возвращать список ссылок на каждый сезон,
    # а не одну ссылку как было раньше
    @classmethod
    def parse(cls, response, dict_gen, film, **kwargs):
        obj = cls(response, film)
        resp_list = []
        type_robot = obj.get_type()
        films_list = obj.get_link(**kwargs)
        price, price_type = obj.get_price(**kwargs)
        value = obj.get_value(**kwargs)
        if film.type == APP_FILM_SERIAL:
            resp_dict = dict_gen(film)
            for serial_season in films_list:
                resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON
                resp_dict['type'] = type_robot
                resp_dict['number'] = serial_season['season']
                resp_dict['value'] = value
                resp_dict['url_view'] = serial_season['season_url']
                resp_dict['price'] = price
                resp_dict['episode'] = 0
                resp_list.append(resp_dict)
                for episode in serial_season['episode_list']:
                    resp_dict = dict_gen(film)
                    resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE
                    resp_dict['type'] = type_robot
                    resp_dict['number'] = serial_season['season']
                    resp_dict['value'] = value
                    resp_dict['url_view'] = episode['url']
                    resp_dict['price'] = price
                    resp_dict['episode'] = episode['number']
                    resp_list.append(resp_dict)
        else:
            resp_dict = dict_gen(film)
            resp_dict['type'] = type_robot
            resp_dict['number'] = 0
            resp_dict['value'] = value
            resp_dict['url_view'] = films_list
            resp_dict['price'] = price
            resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM
            resp_dict['episode'] = 0
            resp_list.append(resp_dict)

        return resp_list
