# coding: utf-8

from django.db import models

from app.users import Users
from apps.films.models import Films,Seasons

# Create your models here.

class Content(models.Model):

    """
    film_id

    name str
    name_orig

    sNumber sint

    description
    ReleaseDate

    seasonid nullable id

    viewer count integer

    viewer_lastweek_cnt
    viewed_lastmonth_cnt

    """

    Film_id = models.ForeignKey(Films)
    name = models.CharField(max_length = 255, verbose_name =u'Название')
    name_orig = models.CharField(max_length = 255 verbose_name =u'Оригинальное название' )
    sNumber = models.IntegerField( verbose_name =u'Номер сезона', null = True, blank =True)
    description = models.TextField(verbose_name =u'Описание')
    ReleaseDate = models.DateTimeField(verbose_name =u'Дата выхода')
    # Поскольку контент может быть как сериал так и фильм, то для контента для которого
    # сезоны не определены Season_id должен быть NULL
    Season_id = models.ForeignKey(Seasons, null = True, blank = True verbose_name =u'Сезоны')
    viewer_cnt = models.IntegerField(verbose_name =u'Количество посмотревших за все время')
    viewer_lastweek_cnt = models.IntegerField(verbose_name =u'Количество посмотревших за последнюю неделю')
    viewer_lastmonth_cnt = models.IntegerField(verbose_name =u'Количество посмотревших за последний месяц')
    
class Locations(models.Model):
    '''
    content_id

    lType str
    lang str
    quality str
    subtitles str
    price float
    price_type str
    value str
    '''

    
    Content_id = models.ForeignKey(Content)
    lType =models.CharField(max_length = 255,verbose_name =u'Тип' )
    quality = models.CharField(max_length=40,verbose_name =u'Качество')
    subtitles = models.CharField(max_length=40,verbose_name =u'Субтитры')
    price = models.FloatField(verbose_name =u'Цена')
    price_type = models.CharField(max_length=40,verbose_name =u'Тип цены')
    value = models.CharField(max_length=40,verbose_name =u'Ценность')
    


class Comments(models.Model):

    User_id = models.ForeignKey(Users)
    Content_id = IntegerField(verbose_name =u'')
    cText = TextField(verbose_name =u'')
    parent_id = IntegerField(verbose_name =u'')
    cStatus = CharField(max_length=40,verbose_name =u'')
    created = DateTimeField(auto_now_add=True,verbose_name =u'')
    
    
