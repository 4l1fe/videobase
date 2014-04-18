from parse_search_page import parse_search_page
from parse_page import parse_page,form_url_from_name


class PlayfamilyParser(object):

    
    def parse(self,html,dict_gen,film,url):

        if html.page_type == 'film_page':

            d = dict_gen(film)

            data = parse_page(html)
            d['price'] = data[0]
            d['price_type'] = 0
            d['url_view'] = form_url_from_name(film.name_orig)
            yield d

        if html.page_type == 'search_page':

            for data in parse_search_page(html):

                if film.name.lower().strip() == data[0]:
                    d = dict_gen(film)

                    d['price'] = data[2]
                    d['price_type'] = 0
                    d['url_view'] = data[1]

                    yield d 

                