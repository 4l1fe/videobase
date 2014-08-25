# coding: utf-8
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.films.models import PersonsFilms
from apps.films.forms import PersonFilmographyApiForm
from apps.films.constants import APP_FILM_PERSON_TYPES_OUR
from apps.films.api.serializers import vbFilm

from videobase.settings import DEFAULT_REST_API_RESPONSE

class PersonFilmographyAPIView(APIView):

    def get(self, request, resource_id, format=None):
        form = PersonFilmographyApiForm(data=request.GET.copy())
        if form.is_valid():
            try:
                c_d = form.cleaned_data
                pfs = PersonsFilms.objects.filter(person__id=resource_id)
                if c_d['type'] != 'all':
                    pfs = pfs.filter(p_type=dict(APP_FILM_PERSON_TYPES_OUR)[c_d['type']])
                films = [pf.film for pf in pfs]
                page = Paginator(films, per_page=c_d['per_page']).page(c_d['page'])
                data = vbFilm(page.object_list, request=self.request, many=True).data
                result = {
                    'total_cnt': page.paginator.count,
                    'per_page': page.paginator.per_page,
                    'page': page.number,
                    'items': data,
                }
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

        return Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_400_BAD_REQUEST)
