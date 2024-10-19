from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from rest_api.internal.v1.user.serializers.profile import UserProfileSerializer
from user.models import UserProfile


class ProfileViewSet(GenericViewSet, ):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['GET'])
    def profile(self, request):
        profile = request.user.profile

        serializer = self.get_serializer(profile)

        return Response(status=HTTP_200_OK, data=serializer.data)
