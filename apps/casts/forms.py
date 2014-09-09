# coding: utf-8
from django.forms import Form
from django.forms import fields

class CastChatSendForm(Form):
    """
    Форма для комментария
    """

    text = fields.CharField(max_length=255, help_text=u'Комментарий')


class CastRatingForm(Form):
    """
    Форма для рейтинга
    """

    rating = fields.IntegerField(help_text=u'Рейтинг')


class CastsListFormBase(Form):
    id         = fields.IntegerField(min_value=0, required=False)
    text       = fields.CharField(max_length='255', required=False)
    pg_rating  = fields.CharField(max_length='255', required=False)
    status     = fields.CharField(max_length='255', required=False)
    service    = fields.CharField(max_length='255', required=False)
    price_type = fields.IntegerField(min_value=0, required=False)
    price_low  = fields.IntegerField(min_value=0, required=False)
    price_high = fields.IntegerField(min_value=0, required=False)
    start_in   = fields.IntegerField(min_value=0, required=False)
    subscribed = fields.BooleanField(required=False)
    
    
    
    def __init__(self, *args, **kwargs):
        super(CastsListFormBase, self).__init__(*args, **kwargs)

        for k,v in self.fields.items():
            if k in kwargs['data'] and kwargs['data'][k]:
                if self.fields[k].required == False:
                    self.fields[k].required = True


    class Meta:
        fields = ('id', 'text', 'pg_rating', 'status', 'service', 'price_type','price_low','price_high','start_in','subscribed')


class CastsChatGetForm(Form):
    id_low  = fields.IntegerField(min_value=0, required=False)
    id_high = fields.IntegerField(min_value=0, required=False)
    limit   = fields.IntegerField(min_value=0, required=False)
    
    def __init__(self, *args, **kwargs):
        super(CastsListFormBase, self).__init__(*args, **kwargs)

        for k,v in self.fields.items():
            if k in kwargs['data'] and kwargs['data'][k]:
                if self.fields[k].required == False:
                    self.fields[k].required = True


    class Meta:
        fields = ('id_low', 'id_high', 'limit')



        