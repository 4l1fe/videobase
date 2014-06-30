from crawler.playfamily_dot_ru.parse_search_page import  form_search_url
from crawler.playfamily_dot_ru.parse_page import form_url_from_name
from crawler.playfamily_dot_ru.utils import HTML_with_type

from crawler.utils.tor import simple_tor_get_page
from crawler.playfamily_dot_ru.utils import HTML_with_type



class PlayfamilyLoader():
    def __init__(self,film):
        self.film = film

    
    
    def load(self):
        url_from_name = form_url_from_name(self.film.name_orig)
        
        if not url_from_name is None:
            reqobj = simple_tor_get_page(url_from_name)
            html_with_type = HTML_with_type(reqobj.decode('utf-8'))
            len(html_with_type)
            html_with_type.page_type='film_page'
            return {'html':html_with_type, 'url_view':url_from_name, 'url':url_from_name}
        else:
            html_with_type =HTML_with_type(simple_tor_get_page(form_search_url(self.film.name)))
            html_with_type.page_type = 'search_page'
            return {'html':html_with_type, 'url_view':url_from_name, 'url':url_from_name}

def playfamily_loader (film):

    return PlayfamilyLoader(film)

    