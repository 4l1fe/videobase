# coding: utf-8
from apps.casts.models import Casts, CastsLocations, CastsServices, CastExtrasStorage
from apps.casts.constants import APP_CONTENTS_PRICE_TYPE_FREE, APP_CONTENTS_PRICE_TYPE_PAY
from crawler.translation_robot.save_image_for_translation import get_one_google_image_by_query
from django.core.files import File

DEFAULT_PG_RATING = u'16+'


def save_cast_dict(cast_service_name, cast_dict):
    if not Casts.objects.filter(title=cast_dict['title'], start=cast_dict['date']).first():
        cast = Casts(title=cast_dict['title'],
                     title_orig=cast_dict['title'],
                     start=cast_dict['date'],
                     duration=cast_dict['meta'].get('duration', None),
                     description=cast_dict['meta'].get('description', None),
                     pg_rating=DEFAULT_PG_RATING)
        cast.save()

        cast_service = CastsServices.objects.get(name=cast_service_name)


        cast_location = CastsLocations(cast=cast,
                                       cast_service = cast_service,
                                       price_type=APP_CONTENTS_PRICE_TYPE_PAY if cast_dict['price']==0 else APP_CONTENTS_PRICE_TYPE_FREE,
                                       price=cast_dict['price'],
                                       url_view=cast_dict['link'],
                                       value=cast_dict['value'],
        )

        cast_location.save()

        image_path = get_one_google_image_by_query(cast_dict['title'])
        cast_extras_storage = CastExtrasStorage(cast=cast,
                                                name=cast_dict['title'],
                                                name_orig=cast_dict['title']
        )
        cast_extras_storage.save()
        cast_extras_storage.photo.save('wallpapper.jpg', File(image_path))
        print cast_extras_storage.id
    else:
        print 'This broadcast is already stored!'