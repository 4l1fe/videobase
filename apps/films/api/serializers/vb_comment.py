# coding: utf-8

from rest_framework import serializers
from apps.contents.models import Comments


#############################################################################################################
#
class vbComment(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('id', 'films', 'user', 'text', 'created')
