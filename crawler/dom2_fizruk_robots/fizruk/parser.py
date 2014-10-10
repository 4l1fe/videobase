#coding: utf-8
from crawler.dom2_fizruk_robots.fizruk.loader import FizrukLoader
import json
from bs4 import BeautifulSoup
from crawler.dom2_fizruk_robots.dom2.parser import get_valid_date_for_str
from multi_key_dict import multi_key_dict

__author__ = 'vladimir'


class ParseFizruk():
    def __init__(self):
        pass

    @staticmethod
    def parse_all_series():
        all_series_informations = []
        pages = FizrukLoader.get_info_pages()
        for page in pages:
            one_info = ParseFizruk.parse_one_info_page(page)
            all_series_informations = all_series_informations + [one_info]

        return all_series_informations

    @staticmethod
    def parse_one_info_page(page):
        page_info = {
            'label': '',
            'value': '',
            'description': '',
            'date': None,
            'actors': []
        }
        opened_page = open(page)
        json_page = json.load(opened_page)
        beatiful_soup = BeautifulSoup(json_page['html'])
        all = beatiful_soup.find('div', { "id" : "all"})
        content = all.find('div', { "id" : "content"})
        center_block = content.find('div', { "id" : "center-block"})
        date = ParseFizruk.get_date(center_block)
        decription = ParseFizruk.get_description(center_block)
        value = ParseFizruk.get_video_code(center_block)
        caption = ParseFizruk.get_caption(center_block)
        all_tags = ParseFizruk.get_actors_tags(center_block)
        actors_names = ParseFizruk.get_actors_names(all_tags)
        page_info['label'] = caption
        page_info['value'] = value
        page_info['description'] = decription
        page_info['date'] = date
        page_info['actors'] = actors_names
        return page_info

    @staticmethod
    def get_video_code(center_block):
        video_player_now = center_block.find('div', { "id" : "video-player-now"})
        iframe = video_player_now.find('iframe')
        video_link = iframe['src']
        return video_link

    @staticmethod
    def get_actors_tags(center_block):
        actors = []
        video_info = center_block.find('div', { "id" : "video-info"})
        steps = video_info.findAll('div', {"class": "step"})
        for step in steps:
            try:
                a_tags = step.findAll('a')
                for a_tag in a_tags:
                    actors = actors + [a_tag.text]
            except Exception, e:
                continue
        return actors


    @staticmethod
    def get_date(center_block):
        video_info = center_block.find('div', { "id" : "video-info"})
        left = video_info.find('div', { "class" : "left"})
        a = left.find('a')
        text_date = a.text
        return get_valid_date_for_str(text_date)

    @staticmethod
    def get_description(center_block):
        video_info = center_block.find('div', { "id" : "video-info"})
        left = video_info.find('div', { "class" : "left"})
        v_descr = left.find('div', { "class" : "v_descr"})
        description = v_descr.text
        return description

    @staticmethod
    def get_caption(center_block):
        h1 = center_block.find('h1')
        caption = h1.text
        return caption

    @staticmethod
    def get_actors_names(tags):
        actors_names = []
        all_actors = ParseFizruk.get_all_actors()
        for tag in tags:
            try:
                act_name = all_actors[tag]
                if act_name not in actors_names:
                    actors_names = actors_names + [act_name]
                    print act_name
            except KeyError, e:
                continue
        return actors_names


    @staticmethod
    def get_all_actors():
        all_actors = multi_key_dict()
        all_actors[u'Фомин', u'Олег Евгеньевич', u'Дмитрий Нагиев', u'Физрук', u'Фома'] = u'Дмитрий Нагиев'
        all_actors[u'Александра Мамаева', u'Мамаева', u'Саша Мамаева'] = u'Полина Грец'
        all_actors[u'Валентин Вялых', u'Усач'] = u'Даниил Вахрушев'
        all_actors[u'Антон Борисов', u'Борзый'] = u'Артур Сопельник'
        all_actors[u'Александр Бодягин', u'Банан'] = u'Андрей Крыжний'
        all_actors[u'Алена Лазукова', u'Пупок'] = u'Виктория Клинкова'
        all_actors[u'Татьяна Александровна', u'Анастасия Панина'] = u'Анастасия Панина'
        all_actors[u'Светлана Петровна', u'Светик'] = u'Карина Мишулина'
        all_actors[u'Лев Романович'] = u'Евгение Кулаков'
        all_actors[u'Эльвира Петровна', u'Завуч'] = u'Елена Муравьева'
        all_actors[u'Слава', u'Славян'] = u'Владимир Жеребцов'
        all_actors[u'Виктор Николаевич', u'Мамай', u'Александр Гордон'] = u'Александр Гордон'
        all_actors[u'Алексей Алексеич', u'Лёха', u'Псих'] = u'Владимир Сычев'
        all_actors[u'Полина'] = u'Оксана Сидоренко'
        return all_actors
