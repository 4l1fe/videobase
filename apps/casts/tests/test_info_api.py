#coding: utf-8

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APISimpleTestCase

from apps.casts.tests.factories import TagFactory, CastsFactory


class CastTestCase(APISimpleTestCase):

    def setUp(self):
        self.tags = [TagFactory.create()]
        self.cast = CastsFactory.create(tags=self.tags)

    def test_info(self):
        response = self.client.get(reverse('cast_info_view', kwargs={'cast_id': self.cast.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
