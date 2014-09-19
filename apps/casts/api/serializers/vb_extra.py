from rest_framework import serializers
from apps.casts.models import CastExtrasStorage


#############################################################################################################
#
class vbExtra(serializers.ModelSerializer):

    url  = serializers.SerializerMethodField('calc_release')

    def calc_url():
        pass
    class Meta:
        model = CastExtrasStorage
        
        fields = ('id', 'name', 'url')
