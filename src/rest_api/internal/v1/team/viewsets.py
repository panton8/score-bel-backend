from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_api.internal.v1.team.serializers import TeamSerializer, TournamentSerializer, MatchSerializer
from team.filters import MatchFilter
from team.models import Team, Tournament, Match
from rest_framework.permissions import AllowAny

from team.services.team_manager import TeamManager


class TournamentViewSet(GenericViewSet, ListModelMixin):
    queryset = Tournament.objects.all().order_by('ordering')
    serializer_class = TournamentSerializer
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['GET'])
    def table(self, request, *args, **kwargs):
        tournament = self.get_object()
        teams = TeamManager().get_actual_tournament_table(tournament)
        table = TeamSerializer(teams, many=True).data
        return Response(table, status=status.HTTP_200_OK)


class TeamViewSet(GenericViewSet, ListModelMixin):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (AllowAny,)


class MatchViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Match.objects.all().order_by('tournament', 'start_time')
    serializer_class = MatchSerializer
    permission_classes = (AllowAny,)
    filterset_class = MatchFilter
