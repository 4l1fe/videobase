# coding: utf-8

from django.contrib import admin
from models import *

#############################################################################################################
# Администрирование пользователей
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'firstname', 'email', 'created', 'ustatus')
    list_per_page = 30

#############################################################################################################
# Отношения пользователей
class UsersRelsAdmin(admin.ModelAdmin):
    pass

#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Users, UsersAdmin)
admin.site.register(UsersRels, UsersRelsAdmin)
