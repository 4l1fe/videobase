# coding: utf-8

from django.contrib import admin

from apps.films.models import *
from apps.films.forms import *


#############################################################################################################
# Администрирование таблицы стран
class CountriesAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Администрирование таблицы жанров
class GenresAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Администрирование таблицы фильмов
class FilmsAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Администрирование таблицы
class UserFilmsAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Администрирование таблицы Доп. материалов к фильмам
class FilmExtrasAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Администрирование таблицы сезонов для сериалов
class SeasonsAdmin(admin.ModelAdmin):
    form = SeasonsAdminForm


#############################################################################################################
# Аминистрирование таблицы Персон
class PersonsAdmin(admin.ModelAdmin):
    list_filter = ('id', 'name', 'name_orig',)
    search_fields = ('id', 'name', 'name_orig',)


#############################################################################################################
# Аминистрирование таблицы Расширения персон
class PersonsExtrasAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Администрирование таблицы Связи фильмов с актерами
class PersonsFilmsAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Countries, CountriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Films, FilmsAdmin)
admin.site.register(UsersFilms, UserFilmsAdmin)
admin.site.register(FilmExtras, FilmExtrasAdmin)
admin.site.register(Seasons, SeasonsAdmin)
admin.site.register(Persons, PersonsAdmin)
admin.site.register(PersonsExtras, PersonsExtrasAdmin)
admin.site.register(PersonsFilms, PersonsFilmsAdmin)
