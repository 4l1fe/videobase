# coding: utf-8
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.forms import UserUpdateForm
from apps.users.models import UsersProfile, User


class UserInfoView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        result = {
            'name': user.profile.nickname,
            'id': user.pk,
            'email': user.email,
        }
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request, format=None, *args, **kwargs):
        form = UserUpdateForm(request.DATA)
        user = request.user
        profile, flag = UsersProfile.objects.get_or_create(user=user)
        if form.is_valid():
            try:
                nickname = form.cleaned_data.get('nickname', None)
                profile.nickname = nickname or profile.nickname
                email = form.cleaned_data.get('email', None)
                user.email = email or user.email
                user.save()
                profile.save()
            except Exception as e:
                Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None, *args, **kwargs):
        password = User.objects.make_random_password()
        user = request.user
        user.set_password(password)
        user.save()
        return Response({'password': password}, status=status.HTTP_200_OK)