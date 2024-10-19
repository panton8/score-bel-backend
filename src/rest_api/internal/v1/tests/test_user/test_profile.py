from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.test import APIClient

from rest_api.testing.api_test_case import ApiTestCase
from rest_api.testing.entity_test_api import EntityTestApi
from user.models import User, UserProfile
from user.testing.factories import UserFactory, UserProfileFactory


class UserProfileTestApi(EntityTestApi):
    entity = 'internal_api:v1:user_profile'


class UserProfileTestCase(ApiTestCase):

    def setUp(self):
        self.client = APIClient()
        self.api = UserProfileTestApi(self.client)

    def test_sign_in__correct_data__ok(self):
        user = UserFactory()
        UserProfileFactory(user=user)
        self.api.client.force_authenticate(user=user)

        rsp = self.api.list_get_action('profile')

        self.assertEqual(rsp['username'], user.username)
