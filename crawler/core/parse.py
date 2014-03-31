# coding: utf-8


# Базовый класс парсера для страници
class BaseParse(object):
    def __init__(self, html):
        self.html = html

    # Стоимость и варианты оплаты (подписка/просмотр/бесплатно)
    def get_cost(self):
        raise NotImplementedError()

    # Доступные серии для просмотра
    def get_series(self):
        raise NotImplementedError()

    # Ссылка на просмотр
    def get_link(self):
        raise NotImplementedError()

    @classmethod
    def parse(cls, html):
        obj = cls(html)
        resp_dict = {
            'cost': obj.get_cost(),
            'series': obj.get_series(),
            'link': obj.get_link(),
        }
        return resp_dict
