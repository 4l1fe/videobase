# coding: utf-8

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.casts.models import Casts, UsersCasts 
from apps.casts.forms import CastRatingForm


################################################################################
class CastsRatingView(APIView):
    """
    Cast info
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, cast_id, *args, **kwargs):
        try:
            user_cast = UsersCasts.objects.get(cast__id=cast_id, user__id=request.user.id)
            return Response({'rating': user_cast.rating}, status=status.HTTP_200_OK)

        except Casts.DoesNotExist:
            return Response({'rating': None}, status=status.HTTP_200_OK)

    def post(self, request, cast_id, *args, **kwargs):
        try:
            user_cast = UsersCasts.objects.get(cast__id=cast_id, user__id=request.user.id)
        except UsersCasts.DoesNotExist:
            try:
                cast = Casts.objects.get(pk=cast_id)
            except Casts.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)

            user_cast = UsersCasts(cast=cast, user=request.user)

            form = CastRatingForm(request.POST)
            if form.is_valid():
                user_cast.rating = form.cleaned_data['rating']
                user_cast.save()
                return Response({'rating': user_cast.rating}, status=status.HTTP_200_OK)

            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cast_id, *args, **kwargs):
        try:
            user_cast = UsersCasts.objects.get(cast__id=cast_id, user__id=request.user.id)
            user_cast.rating = None
            user_cast.save()

            return Response({'rating': user_cast.rating}, status=status.HTTP_200_OK)

        except Casts.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
