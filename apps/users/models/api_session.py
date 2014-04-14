# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from ..constants import *
from django.db import models
from django.conf import settings
import binascii
import os
import  datetime
from hashlib import sha1
from django.conf import settings
from django.utils import timezone

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

################################################################################
# Модель сессий для доступа через API

def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if type(auth) == type(''):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth








class SessionToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(User, verbose_name= 'Session User')
    created = models.DateTimeField(auto_now_add=True)

    #class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/tomchristie/django-rest-framework/issues/705
    #    abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(SessionToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20))

    def __unicode__(self):
        return self.key
    class Meta:
        # Имя таблицы в БД
        db_table = 'users_api_session_tokens'
        app_label = 'users'
        verbose_name = u'API сессия'
        verbose_name_plural = u'API Сессии'


class MultipleTokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    model = SessionToken
    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'x-vb-token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        try:
            uas = UsersApiSessions.objects.get(token = token)

            if uas.get_expiration_time() > timezone.now():
                raise exceptions.AuthenticationFailed('Session expired')
        except UsersApiSessions.DoesNotExist:
            raise exceptions.AuthenticationFailed('There is no session associated with this token')


        return (token.user, token)

    def authenticate_header(self, request):
        return 'X-VB-Token'

class UsersApiSessions(models.Model):

    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    token = models.ForeignKey('SessionToken')

    def get_expire_time(self):
        pass
    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.user.name)

    def get_expiration_time(self):

        return self.created + datetime.timedelta(minutes=settings.API_SESSION_EXPIRATION_TIME)
    class Meta:
        # Имя таблицы в БД
        db_table = 'users_api_sessions'
        app_label = 'users'
        verbose_name = u'API сессия'
        verbose_name_plural = u'API Сессии'







'''
#Based on http://stackoverflow.com/questions/14567586/token-authentication-for-restful-api-should-the-token-be-periodically-changed
class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        # This is required for the time comparison
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - timedelta(hours=24):
            raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.object['user'])

            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow()
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()

'''