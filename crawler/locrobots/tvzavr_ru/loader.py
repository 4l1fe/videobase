# coding: utf-8
import urllib
import time
from crawler.core import BaseLoader
from crawler.core.exceptions import NoSuchFilm
from crawler.tvzavr_ru.parsers import parse_source
from selenium import webdriver
from pyvirtualdisplay import Display


HOST = 'http://www.tvzavr.ru'
URL_LOAD = ''


class Tvzavr_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(Tvzavr_Loader, self).__init__(film, host, url_load)

    def get_url(self, load_function):

        
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = webdriver.Firefox()
        browser.get(self.host)
        time.sleep(2)
        browser.find_element_by_id('search_box').send_keys(self.film.name)
        browser.find_element_by_id('search_button').click()
        time.sleep(2)
        source = browser.page_source
        browser.quit()
        display.stop()
        
        time.sleep(2)
        film_link = parse_source(source, self.film.name, self.host)
        if film_link is None:
            raise NoSuchFilm(self.film)
        return film_link


