# coding: utf-8
import locale

__author__ = 'vladimir'


def convert_orig_month_name_to_lib(month_name):
    if month_name == u'июня':
        return u'Июнь'
    if month_name == u'июля':
        return u'Июль'
    if month_name == u'августа':
        return u'Август'
    if month_name == u'сентября':
        return u'Сентябрь'
    if month_name == u'октября':
        return u'Октябрь'
    if month_name == u'ноября':
        return u'Ноябрь'
    if month_name == u'декабря':
        return u'Декабрь'
    if month_name == u'января':
        return u'Январь'
    if month_name == u'февраля':
        return u'Февраль'
    if month_name == u'марта':
        return u'Март'
    if month_name == u'апреля':
        return u'Апрель'
    if month_name == u'мая':
        return u'Май'

