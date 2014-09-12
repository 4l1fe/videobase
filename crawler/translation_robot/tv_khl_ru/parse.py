# coding: utf-8
from bs4 import BeautifulSoup
import requests

__author__ = 'vladimir'


class TvKHLRuParser():
    def __init__(self):
        pass

    @staticmethod
    def get_time(programma_div):
        b_tag = programma_div.find('b')
        if b_tag:
            return b_tag.getText()
        else:
            return ''

    @staticmethod
    def get_title(programma_div):
        title_div = programma_div.find('span',{ "class" : "name"})
        if title_div:
            return title_div.getText()
        else:
            title_div

    @staticmethod
    def get_description(programma_div):
        descr_div = programma_div.find('div',{ "class" : "previewtext"})
        if descr_div:
            return descr_div.getText()
        else:
            return ''

    @staticmethod
    def get_programs_list_div():
        site_link = 'http://tv.khl.ru/'
        response = requests.get(site_link)
        beatiful_soup = BeautifulSoup(response.content)
        main_div = beatiful_soup.find('div',{ "id" : "main"})
        content_div = main_div.find('div',{ "id" : "content"})
        left_block_div = content_div.find('div',{ "class" : "leftBlock"})
        pguide_div = left_block_div.find('div',{ "class" : "pguide"})
        chanell_act_div = pguide_div.find('div',{ "class" : "chanell act"})
        programs_list_div = chanell_act_div.find('div',{ "class" : "programsList"})
        programs_list = programs_list_div.findAll('div',{ "class" : "progs"})
        active_program = programs_list_div.find('div',{ "class" : "progs active"})
        programs_list.append(active_program)
        return programs_list

    @staticmethod
    def get_translations_for_one_program_date_div(one_day_program_div):
        one_day_programs = one_day_program_div.findAll('div',{ "class" : "programma"})
        streams = []
        for item in one_day_programs:
            time = TvKHLRuParser.get_time(item)
            title = TvKHLRuParser.get_title(item)
            description = TvKHLRuParser.get_description(item)
            print "[#" +time +title + description+ "#]"
            one_stream = {
                'time':time,
                'title':title,
                'description':description
            }
            streams.append(one_stream)
        return streams

    @staticmethod
    def get_translations():
        programs_list = TvKHLRuParser.get_programs_list_div()
        all_streams = []
        for prog_div in programs_list:
            if prog_div:
                streams = TvKHLRuParser.get_translations_for_one_program_date_div(prog_div)
                all_streams = all_streams + streams

        return all_streams

def parse_khl():
    return TvKHLRuParser.get_translations()

