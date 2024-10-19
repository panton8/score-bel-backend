from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.test import APIClient

from rest_api.testing.api_test_case import ApiTestCase
from rest_api.testing.entity_test_api import EntityTestApi
from user.models import User, UserProfile
from user.testing.factories import UserFactory


class UserSignInTestApi(EntityTestApi):
    entity = 'internal_api:v1:user_sign_in'


class UserSignInTestCase(ApiTestCase):

    def setUp(self):
        self.client = APIClient()
        self.api = UserSignInTestApi(self.client)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.password = 'belgium!'
        cls.email = 'super@mail.com'
        cls.username = 'eden_hazard'

    def test_sign_in__correct_data__ok(self):
        user = UserFactory.create(email=self.email)
        user.set_password(self.password)
        user.save()
        data = {
            'email': self.email,
            'password': self.password,
        }

        rsp = self.api.create_entity(entity_data=data, expected_code=HTTP_200_OK)

        self.assertIsNotNone(rsp['refresh'])
        self.assertIsNotNone(rsp['access'])

    def test_sign_up__incorrect_data__no_account(self):
        user = UserFactory.create(email=self.email)
        user.set_password(self.password)
        user.save()
        data = {
            'email': 'fake@gmail.com',
            'password': self.password,
        }

        rsp = self.api.create_entity(entity_data=data, expected_code=HTTP_400_BAD_REQUEST)

        self.assertEqual(rsp[0]['code'], 'user_wrong_credentials')
