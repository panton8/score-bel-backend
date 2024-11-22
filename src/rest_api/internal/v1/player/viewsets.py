from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_api.internal.v1.player.filters import PlayerFilter

from player.models import Player
from player.services.statistics_manager import StatisticsManager
from rest_api.internal.v1.player.serializers import PlayerSerializer, StatisticsSerializer


class PlayerViewSet(GenericViewSet, ListModelMixin):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    permission_classes = [AllowAny]
    filterset_class = PlayerFilter

    @action(detail=True, methods=['GET'], serializer_class=StatisticsSerializer)
    def statistics(self, request, *args, **kwargs):
        player = self.get_object()
        statistics = StatisticsManager(player).get_statistics()
        serializer = self.get_serializer(statistics)
        return Response(serializer.data, status=HTTP_200_OK)
