from django.test import TestCase
from apps.users.models import Users
import copy

from django.db import IntegrityError


class UsersTestCase(TestCase):
    fixtures = ['initial_data.json']
    user = None
    def setUp(self):
        self.features = {
            'firstname': "qwerty",
            'lastname' : "qwerty",
            'email'    : "tumani11@yandex.ru",
            'password' : "1234556",
            'ustatus'  : "1",
            'userpic_type' : "1",
        }

        self.bad_feature = copy.deepcopy(self.features)
        self.bad_feature.update({'email': None})

        self.good_user = Users(**self.features)
        self.bad_user = Users(**self.bad_feature)

    def test_good_create(self):
        try:
            self.good_user.save()
            Users.objects.get(email=self.features['email'])
            # self.assertEqual(True, True)
        except:
            self.assertEqual(True, False)

    def test_bad_create(self):
        with self.assertRaises(IntegrityError):
            self.bad_user.save()
            # Users.objects.get(email=self.bad_feature['email'])
            # self.assertEqual(True, True)
        # except:
        #     self.assertEqual(False, False)