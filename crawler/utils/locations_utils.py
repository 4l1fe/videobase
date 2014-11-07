from apps.contents.models import Contents, Locations
from apps.films.models import Seasons
from apps.robots.constants import APP_ROBOT_VALUE
from django.core.validators import URLValidator
from apps.contents.constants import APP_CONTENTS_PRICE_TYPE_FREE
from django.utils import timezone
from crawler.locations_saver import save_location_to_locs_dict


def sane_dict(film=None):
    '''
    Template for dict returned by parsers with sane defaults
    '''
    return {'film': film,
            'name': film.name,
            'name_orig': film.name_orig,
            'number': None,
            'description': film.description,
            'release_date': film.release_date,
            'series_cnt': None,
            'viewer_cnt': 0,
            'viewer_lastweek_cnt': 0,
            'viewer_lastmonth_cnt': 0,
            'price': 0,
            'price_type': APP_CONTENTS_PRICE_TYPE_FREE,
            'url_view': '',
            'quality': '',
            'subtitles': '',
            'url_source': '',
            'value': '',
            'type': '',
            'episode': '',
            'content_type': ''
            }


def get_content(film, kwargs):
    '''
    Finds or creates content with this film.

    If there are

    number,release_data,description in kwargs then Contents
    object will be created with these defaults
    '''
    # Getting all content with this film
    contents = Contents.objects.filter(film=film)

    if 'number' in kwargs:
        season_num = kwargs['number']
    else:
        season_num = None

    if 'release_date' in kwargs:
        release_date = kwargs['release_date']
    else:
        release_date = None

    if 'description' in kwargs:
        description = kwargs['description']
    else:
        description = None

    if len(contents) == 0:
        #If there is no such content just creating one with meaningful defaults

        if (season_num is None) or (season_num ==0):

            content = Contents(film=film, name=film.name, name_orig=film.name_orig,
                           description=description,
                           release_date=film.release_date,
                           viewer_cnt=0,
                           viewer_lastweek_cnt=0,
                           viewer_lastmonth_cnt=0)
            content.save()

            return content
        else:
            raise NameError(u"Variant with new series currently not in db is not implemented")

    else:
        print season_num
        #According to contract we agreed if there are no seasons there should be return 0, buy some code may return None
        if (season_num is None) or (season_num == 0):
            content = contents[0]
        else:
            content = next((c for c in contents if c.season.number == season_num), None)

            if content is None:

                precontent = contents[0]
                if release_date is None:
                    print u"Assigned release date for new content based on release date for the film %d" %   film.pk
                    release_date = film.release_date

                if 'series_cnt' in kwargs:
                    series_cnt = kwargs['series_cnt']
                else:
                    print u"Assigned new series count in season to number of series in previous season for season %d for film %d" % ( season_num, film.pk)
                    series_cnt = precontent.season.series_cnt

                season = Seasons(film=film, release_date=release_date,
                                 series_cnt=series_cnt, description=description,
                                 number=season_num)
                content = Contents(film=film, name=precontent.name,
                                   name_orig=precontent.name_orig,
                                   description=description, number=season_num,
                                   release_date=release_date,
                                   viewer_cnt=kwargs['viewer_cnt'],
                                   season=season,
                                   viewer_lastweek_cnt=kwargs['viewer_cnt'],
                                   viewer_lastmonth_cnt=kwargs['viewer_cnt'])
                content.save()
        return content


def save_location(film, **kwargs):

    '''
    Creating content if necessary and creating location

    for given dictionary based on one produced by sane_dict
    '''

    locations_d = {
        'info': [],
        'type': kwargs['type']
                }

    if kwargs['type'] in APP_ROBOT_VALUE and kwargs['value'] == '':
        return

    content = get_content(film, kwargs)
    val = URLValidator()

    # Validating that given url_view exists
    val(kwargs['url_view'])
    try:
        prev_location = Locations.objects.get(type=kwargs['type'], content = content)
        print "Found location with such type and film."
    except Locations.DoesNotExist:
        print "There is no location with such type and film."
        prev_location = None
    except Locations.MultipleObjectsReturned:
        print "There are multiple locations with such parameters. Deleting all"
        locations = Locations.objects.filter(type=kwargs['type'], content = content)
        locations.delete()
        prev_location = None


    location = Locations(content=content,
                         type=kwargs['type'],
                         value=kwargs['value'],
                         url_view=kwargs['url_view'],
                         quality=kwargs['quality'],
                         subtitles=kwargs['subtitles'],
                         price=kwargs['price'],
                         price_type=kwargs['price_type'],
                         episode=kwargs['episode'],
                         content_type=kwargs['content_type']

                         
    )
    print "Saving location"
    location.save()
    if prev_location:
        print "Deleting previous location"
        prev_location.delete()

    print u"Saved location for film {}".format(film)
    if prev_location:
        is_new = False
    else:
        is_new = True
    save_location_to_locs_dict(locations_d, True, film, kwargs['type'], location.id, is_new)
    return  locations_d