# coding: utf-8


# Базовый класс парсера для страници
class BaseParse(object):
    def __init__(self, html):
        self.html = html

    # Стоимость и варианты оплаты (подписка/просмотр/бесплатно)
    def get_price(self, **kwargs):
        raise NotImplementedError()

    # Доступные серии для просмотра
    def get_seasons(self, **kwargs):
        raise NotImplementedError()

    # Ссылка на просмотр
    def get_link(self, **kwargs):
        raise NotImplementedError()

    def get_value(self, **kwargs):
        raise NotImplementedError()

    def get_type(self, **kwargs):
        raise NotImplementedError()

    @classmethod
    def parse(cls, response, dict_gen, film, **kwargs):
        obj = cls(response)
        resp_list = []
        type_robot = obj.get_type()
        link = obj.get_link(**kwargs)
        price, price_type = obj.get_price(**kwargs)
        seasons = obj.get_seasons(**kwargs)
        value = obj.get_value(**kwargs)
        if seasons:
            for season in seasons:
                resp_dict = dict_gen(film)
                resp_dict['type'] = type_robot
                resp_dict['number'] = season
                resp_dict['value'] = value
                resp_dict['url_view'] = link
                resp_dict['price'] = price
                resp_dict['price_type'] = price_type
                resp_list.append(resp_dict)

        return resp_list
