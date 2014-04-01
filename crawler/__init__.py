# Crawler module


class Robot(object):
    def __init__(self, loader, parser, films):
        self.loaders = {film: loader(film) for film in films}
        self.parser = parser

    def get_data(self):
        for film in self.loaders:
            d = self.loaders[film].load()
            data = self.parser.parse(d['html'])
            data['url_load'] = d['url']
            yield data