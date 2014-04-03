# coding: utf-8


class RetrievePageException(Exception):
    def __init__(self, url, status_code):
        self.url = url
        self.status_code = status_code


class NoSuchFilm(Exception):
    def __init__(self, film):
        self.film = film