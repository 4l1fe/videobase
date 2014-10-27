#coding: utf-8
import json
from time import sleep, time
from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver
from crawler.tasks.save_location_task import *
from apps.films.models import Films
from crawler.utils.locations_utils import sane_dict


__author__ = 'vladimir'


class VKParser():
    def __init__(self):
        self.phone = '+79296164942'
        self.password = 'beautifulsoup'
        self.id = '4601570'
        self.secret = 'Nr0GOleKVe9u20X6wAZu'
        self.access_token = '57c4c0db57c4c0db5795d861155782f639557c457c4c0db038c6e59a023f8f0e7d9c3bd'
        self.driver = None

    def start_vk_parsing(self):
        self.auth()
        i = 0
        try:
            for film in Films.objects.all():
                if i > 25:
                    break
                founded_video = self.find_video_by_name(film.name)
                if founded_video:
                    data = self.film_dict(film, founded_video)
                    save_location_from_robo_task.apply_async((data,))
                    print founded_video['title'], founded_video['duration'], founded_video['link']
                i += 1
        finally:
            self.disconnect()

    def film_dict(self, film, founded_video):
        resp_dict = sane_dict(film)
        resp_dict['url_view'] = founded_video['link']
        resp_dict['price'] = 0
        resp_dict['type'] = 'vk'
        return resp_dict

    def update_access_token(self):
        ''' Обновление токена по id  и секретному ключу '''
        r = requests.get('https://oauth.vk.com/token?grant_type=password&client_id=4601570&client_secret=Nr0GOleKVe9u20X6wAZu&username=id274312046&password=beautifulsoup')
        #r = requests.get('https://oauth.vk.com/access_token?client_id='+ self.id +'&client_secret=' + self.secret +'&v=5.1&grant_type=client_credentials')
        self.access_token = json.loads(r.content)['access_token']
        print "Token has been updated"

    def create_query(self, method_name, parameters_str):
        return 'https://api.vk.com/method/{}?{}&access_token={}'.format(method_name, parameters_str, self.access_token)

    def get_videos_by_name(self):
        query = self.create_query('video.search', 'q=The beatles')
        r = requests.get(query)
        print r.content

    def auth(self):
        self.driver = webdriver.Firefox()
        redirect_url = 'https://vk.com/id274312046'
        self.driver.get("https://oauth.vk.com/authorize?client_id={}&scope=videoS&redirect_uri={}&display=page&v=5.25&response_type=token".format(
            self.id, redirect_url
        ))
        elem = self.driver.find_element_by_name("email")
        elem.send_keys(self.phone)
        elem = self.driver.find_element_by_name("pass")
        elem.send_keys(self.password)
        self.driver.find_element_by_id('install_allow').click()
        sleep(3)

    def disconnect(self):
        self.driver.close()

    def find_video_by_name(self, name):
        video_url = 'https://vk.com/video'
        self.driver.get(video_url)
        elem = self.driver.find_element_by_id("v_search")
        sleep(2)
        elem.send_keys(name) #.decode('UTF-8')
        sleep(2)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Long')]").click()
        sleep(2)
        videos = self.get_all_videos_info(self.driver.page_source)
        one_video = self.get_one_appropriate_video(videos)
        return one_video

    def get_all_videos_info(self, page):
        videos = []
        base_link = 'https://vk.com'
        bs = BeautifulSoup(page)
        videos_main_conts = bs.findAll('div', {"class": "video_row_inner_cont"})
        for vcont in videos_main_conts:
            short_link = vcont.find('a')['href']
            title = vcont.find('div', {"class": "video_raw_info_name"}).get_text()
            duration = vcont.find('div', {"class": "video_row_duration"}).get_text()
            video_info = {
                'title': title,
                'link': base_link + short_link,
                'duration': duration
            }
            videos = videos + [video_info]
        return videos

    def get_one_appropriate_video(self, videos):
        for video in videos:
            if int(video['duration'].replace(':', '')) > 5500:
                return video
        return None



