# coding: utf-8

from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from apps.films.models import *
from apps.films.forms import *


#############################################################################################################
# Администрирование таблицы стран
class CountriesAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name',)


#############################################################################################################
# Администрирование таблицы жанров
class GenresAdmin(TreeAdmin):
    search_fields = ('id', 'name',)
    form = movenodeform_factory(Genres)


#############################################################################################################
# Администрирование таблицы фильмов
class FilmsAdmin(admin.ModelAdmin):
    form = FilmsAdminForm
    list_filter = ('type', 'release_date',)
    search_fields = ('name', 'type', 'release_date',)


#############################################################################################################
# Администрирование таблицы
class UsersFilmsAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'film',)


#############################################################################################################
# Администрирование таблицы Доп. материалов к фильмам
class FilmExtrasAdmin(admin.ModelAdmin):
    form = FilmExtrasImageForm
    raw_id_fields = ('film',)
    search_fields = ('film__name', 'film__name_orig',)
    list_filter = ('type', )


#############################################################################################################
# Администрирование таблицы сезонов для сериалов
class SeasonsAdmin(admin.ModelAdmin):
    form = SeasonsAdminForm
    raw_id_fields = ('film',)
    search_fields = ('film__name',)
    list_filter = ('release_date',)


#############################################################################################################
# Аминистрирование таблицы Персон
class PersonsAdmin(admin.ModelAdmin):
    form = PersonsImageForm
    list_display = ('id', 'name', 'name_orig', 'image_file',)
    search_fields = ('id', 'name', 'name_orig',)


#############################################################################################################
# Аминистрирование таблицы Расширения персон
class PersonsExtrasAdmin(admin.ModelAdmin):
    raw_id_fields = ('person',)
    search_fields = ('id', 'person__name',)


#############################################################################################################
# Администрирование таблицы Связи фильмов с актерами
class PersonsFilmsAdmin(admin.ModelAdmin):
    raw_id_fields = ('film', 'person',)
    list_filter = ('p_type',)
    search_fields = ('id', 'film__name', 'person__name')


#############################################################################################################
# Администрирование таблицы Связи пользователей с персонами
class UsersPersonsAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'person',)
    search_fields = ('id', 'person__name',)


#############################################################################################################
# Администрирование таблицы Города
class CitiesAdmin(admin.ModelAdmin):
    raw_id_fields = ('country',)
    search_fields = ('id', 'name', 'name_orig',)


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Countries, CountriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Films, FilmsAdmin)
admin.site.register(UsersFilms, UsersFilmsAdmin)
admin.site.register(FilmExtras, FilmExtrasAdmin)
admin.site.register(Seasons, SeasonsAdmin)
admin.site.register(Persons, PersonsAdmin)
admin.site.register(PersonsExtras, PersonsExtrasAdmin)
admin.site.register(PersonsFilms, PersonsFilmsAdmin)
admin.site.register(UsersPersons, UsersPersonsAdmin)
admin.site.register(Cities, CitiesAdmin)
