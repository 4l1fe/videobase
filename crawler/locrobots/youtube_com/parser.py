# coding: utf-8
import json
from bs4 import BeautifulSoup
import re
import requests
from apps.films.models import Films
from apps.robots.models import Robots
from crawler.locations_saver import save_location_to_list
from crawler.utils.locations_utils import sane_dict, save_location

from apps.contents.constants import APP_CONTENTS_PRICE_TYPE_FREE, APP_CONTENTS_PRICE_TYPE_PAY


__author__ = 'vladimir'

CHANNEL_LINK = u'http://www.youtube.com/user/YouTubeMoviesRU'

class YoutubeChannelParser():
    def __init__(self, data):
        pass

    @staticmethod
    def get_or_create_robot():
        try:
            robot = Robots.objects.get(name="YouTubeMoviesRU")
        except:
            robot = Robots.objects.create(name="YouTubeMoviesRU", last_start='2014-07-01', delay=1440)
            robot.save()
        return robot

    @staticmethod
    def init_or_return_state_for_robot(robot):
        state = robot.state
        d = json.loads(state)
        if type(d) is dict:
            return d
        else:
            return {}

    @staticmethod
    def get_already_saved_channels():
        robot = YoutubeChannelParser.get_or_create_robot()
        state = YoutubeChannelParser.init_or_return_state_for_robot(robot)
        return state

    @staticmethod
    def save_channels_list_to_robot_state(channels_list):
        robot = YoutubeChannelParser.get_or_create_robot()
        state = YoutubeChannelParser.init_or_return_state_for_robot(robot)
        for key, value in channels_list.iteritems():
            try:
                state[key] = value
            except:
                continue
        robot.state = json.dumps(state)
        robot.save()
        print "Robot state was saved"

    @staticmethod
    def get_list_of_channels():
        channels_list = YoutubeChannelParser.get_already_saved_channels()
        domen = u'http://www.youtube.com'
        response = requests.get(CHANNEL_LINK)
        beatiful_soup = BeautifulSoup(response.content)
        divs = beatiful_soup.findAll('div',{ "class" : "yt-lockup-content"})

        for div in divs:
            module = div.find('ul',{ "class" : "yt-lockup-meta-info"})
            if not module:
                continue
            atag = module.find('a', {"class" : "g-hovercard yt-uix-sessionlink yt-user-name spf-link "})
            title = unicode(atag.contents[0])
            link = atag.get('href')
            channels_list[title] = domen + link
        return channels_list

    @staticmethod
    def save_location_for_film(film, link, locations):
        try:
            resp_dict = sane_dict(film)
            price, type = YoutubeChannelParser.get_film_price(link)
            resp_dict['price'] = price
            resp_dict['price_type'] = type
            resp_dict['url_view'] = link
            resp_dict['value'] = link
            resp_dict['type'] = u'YouTubeMoviesRU'
            save_location(**resp_dict)
            save_location_to_list(locations, **resp_dict)

        except Exception, e:
            print e.message

        return locations


    @staticmethod
    def process_all_films_for_channel_name( locations, channel_name=u'DreamWorksFilmsRu'):
        r = requests.get('http://gdata.youtube.com/feeds/api/videos?author=' + channel_name + '&alt=json')
        js = r.json()
        try:
            for entr in js['feed']['entry']:
                title = entr['title']['$t'].encode('UTF-8')
                link = entr['link'][0]['href']
                if YoutubeChannelParser.is_film(title):
                    print '### ' + title, link
                    film = Films.objects.get(name = title)
                    if film:
                        YoutubeChannelParser.save_location_for_film(film, link, locations)
        except Exception:
            pass

    @staticmethod
    def process_channels_list():
        locations = []
        site_name = 'www.youtube.com'
        channels_list = YoutubeChannelParser.get_list_of_channels()
        YoutubeChannelParser.save_channels_list_to_robot_state(channels_list)

        for channel in channels_list:
            YoutubeChannelParser.process_all_films_for_channel_name(locations, channel)
        return site_name, locations

    @staticmethod
    def get_film_price(film_link):
        try:
            response = requests.get(film_link)
            beautiful_soup = BeautifulSoup(response.content)
            div_container = beautiful_soup.body.find('div',{ "id" : "page-container"})
            div_offer = div_container.find('div',{ "id" : "watch-checkout-offers"})
            pre_button_span = div_offer.find('span',{ "class" : "ypc-container ypc-delayedloader-target interim-checkout"})
            button_span = pre_button_span.find('span',{ "class" : "yt-uix-button-content"})
            button_label = button_span.find('span',{ "class" : "button-label"})
            price = YoutubeChannelParser.get_price_from_string(unicode(button_label.contents[0]))
            return price, APP_CONTENTS_PRICE_TYPE_PAY
        except Exception,e:
            print e.message
            return 0, APP_CONTENTS_PRICE_TYPE_FREE

    @staticmethod
    def get_price_from_string(str_price):
        currrency_price = re.split('\s+', str_price, flags=re.UNICODE)[1]
        digit_price = float(currrency_price.replace(',','.'))
        return int(digit_price)

    @staticmethod
    def is_film(title):
        trailers_masks = [u'трейлер', u'trailer']
        check = False
        trailer_title = unicode(title, "utf-8").lower()
        for phrase in trailers_masks:
            if trailer_title.find(phrase) != -1:
                check = True
        if check:
            return False
        else:
            return True