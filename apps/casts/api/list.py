# coding: utf-8

import datetime

from django.core.paginator import Paginator
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from videobase.settings import DEFAULT_REST_API_RESPONSE

from apps.casts.models import Casts
from apps.casts.api.serializers import vbCast
from apps.casts.forms import CastsListFormBase
from apps.casts.constants import APP_CASTS_CASTS_PER_PAGE, APP_CASTS_DEFAULT_PAGE

from utils.common import traceback_own


def ids_tranform(o_search, filter):
    ids = filter['id']

    if type(ids) is int:
        o_search = o_search.filter(pk=ids)
    elif type(ids) is list:
        o_search = o_search.filter(pk__in=ids)

    return o_search


def online():
    return {'start__lte': datetime.datetime.now(), 'start__gte': datetime.datetime.now() - datetime.timedelta(hours=3)}


def future():
    return {'start__gt': datetime.datetime.now()}


def passed():
    return {'start__lt': datetime.datetime.now() - datetime.timedelta(hours=3)}


CAST_FILTER = {
    'online': {
        'status': online,
        'order': 'start'
    },
    'future': {
        'status': future,
        'order': 'start'
    },
    'passed': {
        'status': passed,
        'order': '-start'
    }
}


################################################################################
class CastsListView(APIView):
    """
    List casts
    """

    def __validation_pagination(self, page, per_page, filter):
        try:
            page = int(page)
        except (TypeError, ValueError):
            page = APP_CASTS_DEFAULT_PAGE

        if page < APP_CASTS_DEFAULT_PAGE:
            page = APP_CASTS_DEFAULT_PAGE

        try:
            per_page = int(per_page)
        except (TypeError, ValueError):
            per_page = APP_CASTS_CASTS_PER_PAGE

        if 0 < per_page > APP_CASTS_CASTS_PER_PAGE:
            per_page = APP_CASTS_CASTS_PER_PAGE

        filter.update({'per_page': per_page, 'page': page})
        return filter


    def validate_tags(self, tag):
        try:
            tag = int(tag)
            return tag
        except ValueError:
            try:
                tag = list(tag)
                return tag
            except ValueError:
                return Response({'error': 'Wrong tags field. Neither int nor list of ints'}, status=status.HTTP_400_BAD_REQUEST)


    def search(self, filter):
        o_search = Casts.search_manager.all()

        def subscribe_calc(o_s, is_subscribed):
            if self.request.user.is_authenticated() and filter.get('recommend'):
                sql = """
                    NOT "casts"."id" IN (
                    SELECT "users_casts"."film_id" FROM "users_casts"
                    WHERE "users_films"."user_id" = %s AND
                          ("users_films"."subscribed" = %s )
                )
                """

                o_s = o_s.extra(
                    where=[sql],
                    params=[self.request.user.pk, is_subscribed],
                )

            return o_s

        transform_map = {
            'id': ids_tranform,
            'text': lambda o_s, arg: o_s.search(arg),
            'status': lambda o_s, arg: o_s.filter(**CAST_FILTER[arg]['status']()).order_by(CAST_FILTER[arg]['order']),
            'pg_rating': lambda o_s, arg: o_s.filter(pg_rating_lte=arg),
            'service': lambda o_s, arg: o_s.filter(cl_location_rel__service=arg),
            'price_type': lambda o_s, arg: o_s.filter(cl_location_rel__price_type=arg),
            'price_low': lambda o_s, arg: o_s.filter(cl_location_rel__price__gte=arg),
            'price_high': lambda o_s, arg: o_s.filter(cl_location_rel__price__lte=arg),
            'start_in': lambda o_s, arg: o_s.filter(start=datetime.datetime.now()+datetime.timedelta(seconds=arg)),
            'tag': lambda o_s, arg: o_s.filter(tags__id=arg),
            'subscribed': subscribe_calc,
            'per_page': lambda o_s, arg: o_s,
            'page': lambda o_s, arg: o_s,
            # TODO Test that it returns correct objects in case of multiple tags per cast
        }

        for field in filter:
            if filter[field]:
                o_search = transform_map[field](o_search, filter[field])
            elif field == 'status':
                o_search = o_search.filter(start__gte=datetime.datetime.now() - timezone.timedelta(hours=3)).order_by('start')

        return o_search

    def get(self, request, *args, **kwargs):
        self.get_copy = request.GET.copy()
        if 'tags' in self.get_copy:
            raise Exception('Need realese')

        form = CastsListFormBase(data=self.get_copy)
        if form.is_valid():
            per_page = self.get_copy.get('per_page')
            page = self.get_copy.get('page')

            filter = self.__validation_pagination(page, per_page, form.cleaned_data)
            per_page = filter['per_page']
            page = filter['page']

            o_search = self.search(filter)
            try:
                page = Paginator(o_search, per_page).page(page)
            except Exception, e:
                traceback_own(e)
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            result = {
                'total_cnt': page.paginator.count,
                'per_page': page.paginator.per_page,
                'page': page.number,
                'items': vbCast(page.object_list, many=True).data,
            }

            return Response(result, status=status.HTTP_200_OK)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
