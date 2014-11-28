# coding: utf-8
import pytz
import datetime
from rest_framework import serializers, ISO_8601
from videobase.settings import TIME_ZONE


class DateTimeWithTimeZone(serializers.DateTimeField):

    def to_native(self, value):
        if isinstance(value, datetime.datetime):
            return pytz.timezone(TIME_ZONE).localize(value, is_dst=None)

        elif self.format.lower() == ISO_8601:
            return value.isoformat()

        else:
            return None