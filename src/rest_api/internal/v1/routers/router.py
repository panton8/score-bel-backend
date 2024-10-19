from rest_framework import routers

from rest_api.internal.v1.user.viewsets.profile import ProfileViewSet
from rest_api.internal.v1.user.viewsets.sign_up import SignUpViewSet
from rest_api.internal.v1.user.viewsets.sign_in import SignInViewSet

router = routers.DefaultRouter()


router.register(r'user/sign-up', SignUpViewSet, basename='user_sign_up')
router.register(r'user/sign-in', SignInViewSet, basename='user_sign_in')
router.register(r'user', ProfileViewSet, basename='user_profile')
