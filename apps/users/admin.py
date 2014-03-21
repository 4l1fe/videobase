# coding: utf-8

from django.contrib import admin
from models import *


#############################################################################################################
# Администрирование таблицы пользователей
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'email', 'created', 'ustatus')
    search_fields = ('id', 'firstname', 'lastname', 'email')
    list_filter = ('created',)
    list_per_page = 30


#############################################################################################################
# Отношения пользователей
class UsersRelsAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Аминистрирование таблицы загружаемых картинок пользователей
class UsersPicsAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Users, UsersAdmin)
admin.site.register(UsersRels, UsersRelsAdmin)
admin.site.register(UsersPics, UsersPicsAdmin)
