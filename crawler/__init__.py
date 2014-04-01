# Crawler module


class Robot(object):
    def __init__(self, loader, parser, films):
        self.loaders = {film: loader(film) for film in films}
        self.parser = parser

    def get_data(self, dict_gen):
        for film in self.loaders:
            html = self.loaders[film].load()
            for data in self.parser.parse(html,dict_gen):
                data['url_load'] = d['url']
                yield data

