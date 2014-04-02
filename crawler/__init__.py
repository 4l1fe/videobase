# Crawler module


class Robot(object):
    def __init__(self, loader, parser, films):
        print loader
        self.loaders = {film: loader(film) for film in films}
        self.parser = parser

    def get_data(self, dict_gen):
        for film in self.loaders:
            d = self.loaders[film].load()
            for data in self.parser.parse(d['html'], dict_gen, film):
                data['url_load'] = d['url']
                yield data

