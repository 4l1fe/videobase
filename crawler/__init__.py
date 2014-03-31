# Crawler module


class Robot(object):
    def __init__(self, loader, parser, films):
        self.loaders = {film: loader(film) for film in films}
        self.parser = parser

    def get_data(self):
        for loader in self.loaders:
            html = loader.load()
            data = self.parser.parse(html)
            yield data