# coding: utf-8

from django.contrib import admin
from models import *

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    pass

admin.site.register(Users, UsersAdmin)