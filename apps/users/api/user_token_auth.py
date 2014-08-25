# coding: utf-8
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authtoken import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from apps.users.models.api_session import UsersApiSessions, SessionToken
from apps.users.api.utils import create_new_session
from videobase.settings import HTTP_USER_TOKEN_TYPE, DEFAULT_REST_API_RESPONSE


class ObtainAuthToken(views.ObtainAuthToken):

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])
            return Response({HTTP_USER_TOKEN_TYPE: token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainSessionToken(APIView):

    def get(self, request, format=None, *args, **kwargs):
        try:
            session = create_new_session(request.user)
            response_dict = {
                'session': session.pk,
                'expires': session.get_expiration_time(),
                'session_token': session.token.key,
            }
        except Exception as e:
            return Response(DEFAULT_REST_API_RESPONSE,status=status.HTTP_404_NOT_FOUND)

        return Response(response_dict, status=status.HTTP_200_OK)

    @permission_classes((IsAuthenticated, ))
    def delete(self, request, format=None, *args, **kwargs):
        token = request.auth
        try:
            session = UsersApiSessions.objects.get(token=token.pk)
            session.active = False
            session.save()
        except UsersApiSessions.DoesNotExist as e:
            return Response({'e': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({},status=status.HTTP_200_OK)


class RevokeSessionToken(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        session_keys = SessionToken.objects.filter(user=user).values_list('key', flat=True)
        UsersApiSessions.objects.filter(token__in=session_keys).update(active=False)
        token = user.auth_token
        token.delete()
        Token.objects.create(user=user)
        return Response(DEFAULT_REST_API_RESPONSE, status = status.HTTP_200_OK)
