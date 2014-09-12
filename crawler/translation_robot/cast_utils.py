# coding: utf-8

from apps.casts.models import Casts, CastsLocations, CastsServices
from apps.casts.constants import APP_CONTENTS_PRICE_TYPE_FREE, APP_CONTENTS_PRICE_TYPE_PAY

def save_cast_dict(cast_service_name,cast_dict):

    cast = Casts(title=cast_dict['title'],
                 title_orig=cast_dict['title'],
                 start=cast_dict['date'],
                 duration=cast_dict['meta'].get('duration', None),
                 description=cast_dict['meta'].get('description', None),
                 pg_rating=cast_dict['meta'].get('description', None))

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


