# coding: utf-8
import requests
import urllib
from bs4 import BeautifulSoup
import json


HOST = 'www.imhonet.ru'
SEARCH = 'search/?{}'


def update_person_info(person, **kwargs):
    search_text = urllib.urlencode({'search': (person.name), 'persons': 'on'})
    search_url = SEARCH.format(search_text)
    url = 'http://%s/%s' % (HOST, search_url)
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    bio = ''
    if soup.find('p', {'class': 'm-searchresult-notfound'}) is None:
        bio = soup.find('p', {'class': 'm-biography-text'})
        if bio:
            bio = bio.text
            if bio.lower().count(person.name.lower()) < 1:
                bio = ''
        else:
            person_div = soup.find('div', {'class': 'm-inlineitemslist-describe'})
            if person_div:
                person_page = person_div.a.get('href')
                content = requests.get(person_page).content
                soup = BeautifulSoup(content)
                bio = soup.find('p', {'class': 'm-biography-text'}).text
                if bio.lower().count(person.name.lower()) < 1:
                    bio = ''
    if not len(bio):
        json_data = open('persons')
        data = json.load(json_data)
        persons = data['results']['bindings']
        for item in persons:
            if person.name.lower().strip() == item['name']['value'].lower().strip():
                bio = item['bio']['value']
    if len(bio):
        person.bio = bio
        person.save()