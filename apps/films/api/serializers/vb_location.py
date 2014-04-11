# coding: utf-8

from rest_framework import serializers
from apps.contents.models import Locations


#############################################################################################################
#
class vbLocation(serializers.ModelSerializer):

    class Meta:
        model = Locations
