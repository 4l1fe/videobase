# Crawler module
import time
import random


class Robot(object):
    def __init__(self, loader, parser, films):
        self.loaders = {film: loader(film) for film in films}
        self.parser = parser

    def get_data(self, dict_gen):
        for film in self.loaders:
            time.sleep(random.randint(1, 16))
            d = self.loaders[film].load()
            for data in self.parser.parse(d['html'], dict_gen, film, url=d['url']):
                data['url_source'] = d['url']
                yield data

