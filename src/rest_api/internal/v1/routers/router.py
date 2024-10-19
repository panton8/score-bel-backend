from rest_framework import routers

from rest_api.internal.v1.user.viewsets.sign_up import SignUpViewSet

router = routers.DefaultRouter()


router.register(r'user/sign-up', SignUpViewSet, basename='user_sign_up')
