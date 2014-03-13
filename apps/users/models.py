# coding: utf-8

from django.db import models
from .constants import *
from users.users_rels import UsersRels

#############################################################################################################
# Пользователи
class Users(models.Model):
    firstname    = models.CharField(max_length=255, verbose_name=u'Имя')
    lastname     = models.CharField(max_length=255, verbose_name=u'Фамилия')
    email        = models.EmailField(max_length=255, unique=True, verbose_name=u'Email')
    passhash     = models.CharField(max_length=255, verbose_name=u'Пароль')
    last_visited = models.DateTimeField(auto_now_add=True, verbose_name=u'Последний визит')
    created      = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    ustatus      = models.PositiveSmallIntegerField(choices=USER_STATUS, verbose_name=u'Статус')
    userpic_type = models.CharField(null=True, blank=True, default=None, choices=USER_PIC_TYPES, max_length=255, verbose_name=u'Тип картинки')
    userpic      = models.ForeignKey('UsersPics', default=None, null=True, blank=True, verbose_name=u'Аватар')

    def __unicode__(self):
        return u'[%s] %s %s' % (self.pk, self.firstname, self.lastname)

    @property
    def name(self):
        return u'%s %s' % (self.firstname, self.lastname)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'


#############################################################################################################
# Запросы пользователей
class UsersRequests(models.Model):
    user    = models.ForeignKey(Users, verbose_name=u'Пользователи')
    hash    = models.IntegerField(verbose_name=u'Запрос')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    rtype   = models.CharField(max_length=255, verbose_name=u'Тип запроса')
    value   = models.CharField(max_length=255, verbose_name=u'Значение запроса')

    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.user.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_requests'
        verbose_name = u'Запросы пользователя'
        verbose_name_plural = u'Запросы пользователей'


#############################################################################################################
# Лог пользователей
class UsersLog(models.Model):
    user    = models.ForeignKey(Users, verbose_name=u'Пользователи')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    itype   = models.CharField(max_length=255, verbose_name=u'Тип')
    iobject = models.CharField(max_length=255, verbose_name=u'Объект')
    itext   = models.CharField(max_length=255, verbose_name=u'Текст')

    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.user.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_logs'
        verbose_name = u'Лог пользователя'
        verbose_name_plural = u'Логи пользователей'


#############################################################################################################
# Картинки пользователей
class UsersPics(models.Model):
    user = models.ForeignKey(Users, verbose_name=u'Пользователи')
    url  = models.CharField(max_length=255, verbose_name=u'Url')


    def __unicode__(self):
        return u'[%s] %s : %s' % (self.pk, self.user.name, self.url)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_pics'
        verbose_name = u'Картинки пользователя'
        verbose_name_plural = u'Картинки пользователей'


#############################################################################################################
# Социальность пользователей
class UsersSocial(models.Model):
    user    = models.ForeignKey(Users, verbose_name=u'Пользователи')
    stype   = models.CharField(max_length=255, verbose_name=u'')
    stoken  = models.CharField(max_length=255, verbose_name=u'')
    suserid = models.IntegerField(verbose_name=u'')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    sphoto  = models.IntegerField(verbose_name=u'')


    def __unicode__(self):
        return u'[%s] %s - %s' % (self.pk, self.user.name, self.stoken)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_socials'
        verbose_name = u'Социальность пользователя'
        verbose_name_plural = u'Социальность пользователей'


#############################################################################################################
# Персоны
class Persons(models.Model):
    name      = models.CharField(max_length=255, verbose_name=u'Имя')
    name_orig = models.CharField(max_length=255, verbose_name=u'Оригинальное имя')
    bio       = models.TextField(verbose_name=u'Биография')
    photo     = models.ImageField(upload_to=PERSON_PHOTO_DIR, blank=True, null=True, verbose_name=u'Фото')


    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.user.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'persons'
        verbose_name = u'Персона'
        verbose_name_plural = u'Персоны'


#############################################################################################################
# Расширения персоны
class PersonsExtras(models.Model):
    person      = models.ForeignKey(Persons, max_length=255, verbose_name=u'Персона')
    etype       = models.CharField(max_length=255, verbose_name=u'')
    name        = models.TextField(verbose_name=u'Имя')
    name_orig   = models.TextField(verbose_name=u'Оригинальное имя')
    description = models.TextField(verbose_name=u'Описавние')
    url         = models.CharField(max_length=255, verbose_name=u'Фото')


    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.person.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'persons_extras'
        verbose_name = u'Расширения персоны'
        verbose_name_plural = u'Расширения персон'


#############################################################################################################
# Таблица связи Пользователей и Персон
class UsersPersons(models.Model):
    user       = models.ForeignKey(Users, max_length=255, verbose_name=u'Пользователи')
    person     = models.ForeignKey(Persons, max_length=255, verbose_name=u'Персона')
    upstatus   = models.IntegerField(verbose_name=u'Статус')
    subscribed = models.IntegerField(verbose_name=u'Подписка')


    def __unicode__(self):
        return u'[%s %s]' % (self.user, self.person)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_persons'
        verbose_name = u'Расширения персоны'
        verbose_name_plural = u'Расширения персон'
