# coding: utf-8


# Базовый класс парсера для страници
class BaseParse(object):
    def __init__(self, html):
        self.html = html

    # Стоимость и варианты оплаты (подписка/просмотр/бесплатно)
    def get_price(self):
        raise NotImplementedError()

    # Доступные серии для просмотра
    def get_seasons(self):
        raise NotImplementedError()

    # Ссылка на просмотр
    def get_link(self):
        raise NotImplementedError()

    @classmethod
    def parse(cls, html, dict_gen):
        obj = cls(html)
        resp_dict = dict_gen()
        seasons = obj.get_seasons()
        link = obj.get_link()
        price, price_type = obj.get_price()
        if seasons:
            for season in seasons:
                resp_dict['numer'] = season
                resp_dict['value'] = link
                resp_dict['price'] = price
                resp_dict['price_type'] = price_type

        return resp_dict
