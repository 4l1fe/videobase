# coding: utf-8
import json
import locale
import os
import urllib2
from bs4 import BeautifulSoup
import datetime
from crawler.dom2_fizruk_robots.dom2.loader import Dom2Loader
from crawler.dom2_fizruk_robots.locale_manager import convert_orig_month_name_to_lib

__author__ = 'vladimir'

#episode = один день


class ParseDom2():
    def __init__(self):
        pass

    @staticmethod
    def parse_all_pages():
        all_episods_info = []
        locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
        pages = []
        pages = Dom2Loader.load_pages()
        all_actors = ParseDom2.get_all_actors()
        i = 0
        for page in pages:
            all_episods_info = all_episods_info + ParseDom2.parse_one_page(page, all_actors)
            i += 1
            if i == 5:
                break
        return all_episods_info

    @staticmethod
    def parse_one_page(page, all_actors):
        episods_informations = []
        opned_page = open(page)
        json_page = json.load(opned_page)
        beatiful_soup = BeautifulSoup(json_page['html'])
        ParseDom2.get_episods_for_page(beatiful_soup)
        episods = ParseDom2.get_episods_for_page(beatiful_soup)
        for episode in episods:
            episod_quick_info = ParseDom2.get_episode_quick_info(episode)
            episods_informations = episods_informations + [ParseDom2.parse_one_episode(episod_quick_info, all_actors)]
        return episods_informations

    @staticmethod
    def get_episods_for_page(soup):
        div_big_panel_content = ParseDom2.get_b_big_panel_content_div(soup)
        div_photos = div_big_panel_content.find('div', {"class": "photos"})
        div_items = div_photos.findAll('div', {"class": "item first"})
        div_items = div_items + div_photos.findAll('div', {"class": "item "})
        return div_items

    @staticmethod
    def parse_one_episode(episod_quick_info, all_actors):
        video_info_page = Dom2Loader.load_video_info_page(episod_quick_info['video_info_page_url'], episod_quick_info['label'])
        if not video_info_page:
            print "No video details page loaded!"
            return
        opned_page = open(video_info_page)
        json_page = json.load(opned_page)
        beatiful_soup = BeautifulSoup(json_page['html'])
        episod_info = ParseDom2.parse_video_page(beatiful_soup)
        episod_info['actors'] = ParseDom2.get_actors_for_episode(episod_info['date'], all_actors)
        return episod_info

    @staticmethod
    def get_episode_quick_info(episode):
        quick_info = {
            'label': '',
            'video_info_page_url': '',
            'poster': '',
        }

        a_tag = episode.find('a', {"class": "imgBox link no-select"})

        quick_info['label'] = unicode(episode.find('div', {"class": "photo-list-title"}).find('a').contents[0])
        quick_info['video_info_page_url'] = 'http://dom2.ru'+a_tag['href']
        poster_link = a_tag.find('img')['src']
        quick_info['poster'] = ParseDom2.save_poster_to_file(poster_link, quick_info['label'])
        return quick_info

    @staticmethod
    def parse_video_page(soup):

        episode_info = {
            'label': '',
            'date': None,
            'description': '',
            'value': '',
            'actors': []
        }
        div_big_panel_content = ParseDom2.get_b_big_panel_content_div(soup)
        photo_panel_table = div_big_panel_content.find('table', {"class": "photo-panel all-height"})

        episode_info['date'] = ParseDom2.get_video_date(photo_panel_table)
        episode_info['label'] = ParseDom2.get_video_label(photo_panel_table)
        print episode_info['label']
        episode_info['description'] = ParseDom2.get_video_description(photo_panel_table)
        episode_info['value'] = ParseDom2.get_video_embedded_code(photo_panel_table)
        return episode_info


    @staticmethod
    def get_actors_for_episode(episode_date, all_actors):
        episode_actors = []
        for actor in all_actors:
            if ParseDom2.is_actor_played(actor, episode_date):
                episode_actors = episode_actors + [actor]
        return episode_actors

    @staticmethod
    def is_actor_played(actor, date):
        if date is None:
            return False
        if (actor['finish_date'] is None) and (actor['start_date'] <= date):
            return True
        if not (actor['finish_date'] is None) and (actor['finish_date'] >= date) and (actor['start_date'] <= date):
            return True
        return False

    @staticmethod
    def get_all_actors():
        old = ParseDom2.get_old_actors()
        current = ParseDom2.get_current_actors()
        all_actors = old + current
        return all_actors

    @staticmethod
    def get_old_actors():
        actors = []
        pages = Dom2Loader.load_old_actors_pages()
        for page in pages:
            actors = actors + ParseDom2.parse_one_actors_page(page)
        return actors

    @staticmethod
    def parse_one_actors_page(page):
        old_actors_from_one_page = []
        opned_page = open(page)
        json_page = json.load(opned_page)
        beatiful_soup = BeautifulSoup(json_page['html'])
        actors_descrs = beatiful_soup.findAll('td', {"class": "descr"})
        for actor in actors_descrs:
            actor_inf = ParseDom2.get_one_actor_info(actor)
            old_actors_from_one_page = old_actors_from_one_page + [actor_inf]
        return old_actors_from_one_page

    @staticmethod
    def get_current_actors():
        current_actors = []
        actorspage = Dom2Loader.load_current_actors_page()
        opned_page = open(actorspage)
        json_page = json.load(opned_page)
        beatiful_soup = BeautifulSoup(json_page['html'])
        actors_descrs = beatiful_soup.findAll('td', {"class": "descr"})
        for actor in actors_descrs:
            actor_inf = ParseDom2.get_one_actor_info(actor)
            current_actors = current_actors + [actor_inf]
        return current_actors

    @staticmethod
    def get_one_actor_info(actor_div):

        actor_info = {
            'name': '',
            'start_date': None,
            'finish_date': None,
            'profile_link': ''
        }

        nik = actor_div.find('a', {"class": "nik"})
        name = nik.text
        profile_link = nik['href']
        div = actor_div.find('div', {"class": "txt"})
        nobrs = div.findAll('nobr')
        actor_info['start_date'] = get_valid_date_for_str(nobrs[0].text)
        if len(nobrs) > 1:
            actor_info['finish_date'] = get_valid_date_for_str(nobrs[1].text)

        actor_info['name'] = name
        actor_info['profile_link'] = 'http://dom2.ru' + profile_link

        return actor_info


    @staticmethod
    def save_poster_to_file(link, name):
        file_name = None
        directory = 'static/upload/dom2'
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            if 'dom2' not in link:
                link = 'http://dom2.ru'+link
            img = urllib2.urlopen(link)
            with open(directory + '/' + name + '.jpg', 'wb') as localFile:
                localFile.write(img.read())
            file_name = name + '.jpg'
        except Exception, e:
            print e.message
            print "Poster saving failed"
        return file_name

    @staticmethod
    def get_video_date(photo_panel_class):
        botton_line_td = photo_panel_class.find('td', {"class": "bottom-line"})
        div_calendar = botton_line_td.find('div', {"class": "calendar-td"})
        div_green_box = div_calendar.find('div', {"class": "greenBox"})
        span_green_box_date = div_green_box.find('span', {"class": "greenBoxDate"})
        a_link = span_green_box_date.find('a', {"class": "link no-select"})
        e_date = get_valid_date_for_str(a_link.find('nobr').text)
        return e_date

    @staticmethod
    def get_video_description(photo_panel_class):
        try:
            div_content_text = photo_panel_class.find('div', {"class": "content-text"})
            p_tag = div_content_text.find('p')
            description = p_tag.text
        except Exception, e:
            description = ''
        return description

    @staticmethod
    def get_video_embedded_code(photo_panel_class):
        div_movie_container = photo_panel_class.findAll('div', {"id": "movieContainer"})
        #print '#', div_movie_container
        #code = div_movie_container.find('embed', {"id": "player"})
        #print "code", code
        return ''#code

    @staticmethod
    def get_video_label(photo_panel_class):
        h2 = photo_panel_class.find('h2')
        label = h2.text
        return label

    @staticmethod
    def get_b_big_panel_content_div(soup):
        main = soup.find('table', {"class": "all"})
        middle_td = main.find('td', {"class": "middle"})
        table = middle_td.find('table', {"class": "bottom-bg"})
        div = table.find('div', {"class": "content max-width"})
        div_content = div.find('div', {"id": "the_content"})
        div_the_content2 = div_content.find('div', {"id": "the_content2"})
        inner_table = div_the_content2.find('table', {"class": "center-content"})
        left_column = inner_table.find('td', {"class": "left-column"})
        div_persent_pad = left_column.find('div', {"class": "percent-pad"})
        center_table = div_persent_pad.find('table', {"class": "center-subcontent"})
        left_slice = center_table.find('td', {"class": "left-slice"})
        div_big_panel = left_slice.find('div', {"class": "b-bigPanel"})
        div_big_panel_content = div_big_panel.find('div', {"class": "b-bigPanel__content"})
        return div_big_panel_content


def get_valid_date_for_str(date_str):
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
    res_date = None
    res_date_text = ''
    dates_parts = date_str.split(' ')
    if len(dates_parts) == 3:
        year = dates_parts[2]
    else:
        year = u'2014'
    if len(dates_parts) == 1:
        if date_str == u'Сегодня':
            day = datetime.datetime.now().day
        elif date_str == u'Вчера':
            day = datetime.date.fromordinal(datetime.date.today().toordinal()-1).day
        res_date_text = str(day) + ' ' + str(datetime.datetime.now().month) + ' ' + year
        res_date = datetime.datetime.strptime(res_date_text.encode("utf-8"), "%d %m %Y").date()
    else:
        try:
            res_date_text = dates_parts[0] + ' ' + convert_orig_month_name_to_lib(dates_parts[1]) + ' ' + year
            res_date = datetime.datetime.strptime(res_date_text.encode("utf-8"), "%d %B %Y").date()
        except ValueError, e:
            res_date_text = u'1' + ' ' + convert_orig_month_name_to_lib(dates_parts[1]) + ' ' + year
            res_date = datetime.datetime.strptime(res_date_text.encode("utf-8"), "%d %B %Y").date()
            print "Datetime converting error: ", dates_parts[0], convert_orig_month_name_to_lib(dates_parts[1]), year
        except Exception, e:
            print e.message
    return res_date
