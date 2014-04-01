from crawler.playfamily_dot_ru.parse_search_page import  form_search_url
from crawler.playfamily_dot_ru.parse_page import form_url_from_name

from crawler.core.browser import simple_get

class HTML_with_type(unicode):
    page_type =None


class Loader():

    def __init__(self,film):
        self.film = film

    self.page_type = None
    
    def load():
        url_from_name = form_url_from_name(self.film.name_orig)
        
        if not url_from_name is None:
            html_with_type = HTML_with_type(simple_get(url_from_name))
            html_with_type.page_type='film_page'
            return html_with_type
        else:
            html_with_type =HTML_with_type(simple_get(form_search_url(self.film.name)))
            html_with_type.page_type = 'search_page'
            return html_with_type

def playfamily_loader (film):

    return Loader(film)

    