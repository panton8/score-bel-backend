from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_api.internal.v1.player.serializers import LineUpSerializer, SummarySerializer
from rest_api.internal.v1.team.serializers import TeamSerializer, TournamentSerializer, MatchSerializer
from team.filters import MatchFilter
from team.models import Team, Tournament, Match
from rest_framework.permissions import AllowAny

from team.services.line_up_manager import LineUpManager
from team.services.summary_manager import SummaryManager
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

    @extend_schema(
        responses={200: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(
            name='match line-up',
            value={"Нёман": {"start": [{"surname": "Савицкий", "position": "mid", "player_number": 10}],
                             "bench": [{"surname": "Варакса", "position": "mid", "player_number": 82}]},
                   "Батэ": {"start": [{"surname": "Скопец", "position": "gkp", "player_number": 99},
                                      {"surname": "Жульпа", "position": "mid", "player_number": 19}],
                            "bench": []}},
        response_only=True)],
    )
    @action(detail=True, methods=['GET'], serializer_class=LineUpSerializer, url_path='line-up')
    def line_up(self, request, *args, **kwargs):
        match = self.get_object()
        line_up_manager = LineUpManager(match)
        home_line_up_start = line_up_manager.get_home_team_line_up()
        away_line_up_start = line_up_manager.get_away_team_line_up()
        home_line_up_bench = line_up_manager.get_home_team_line_up(in_start=False)
        away_line_up_bench = line_up_manager.get_away_team_line_up(in_start=False)

        home_line_up_start_data = [item['player'] for item in self.get_serializer(home_line_up_start, many=True).data]
        away_line_up_start_data = [item['player'] for item in self.get_serializer(away_line_up_start, many=True).data]
        home_line_up_bench_data = [item['player'] for item in self.get_serializer(home_line_up_bench, many=True).data]
        away_line_up_bench_data = [item['player'] for item in self.get_serializer(away_line_up_bench, many=True).data]

        data = {
            match.home_team.name: {'start': home_line_up_start_data, 'bench': home_line_up_bench_data},
            match.away_team.name: {'start': away_line_up_start_data, 'bench': away_line_up_bench_data},
        }

        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(
            name='match summary',
            value={"Днепр": [{"minute": 8, "action": "yellow_card", "major_event_player_name": "Н.Краснов", "minor_event_player_name": None}],
                   "Динамо-Минск": [{"minute": 15, "action": "yellow_card", "major_event_player_name": "Н.Демченко", "minor_event_player_name": None},]},
            response_only=True)],
    )
    @action(detail=True, methods=['GET'], serializer_class=SummarySerializer, url_path='summary')
    def summary(self, request, *args, **kwargs):
        match = self.get_object()
        match_summary_manager = SummaryManager(match)
        home_team_summary = match_summary_manager.get_home_team_summary()
        away_team_summary = match_summary_manager.get_away_team_summary()

        home_team_summary_data = self.get_serializer(home_team_summary, many=True).data
        away_team_summary_data = self.get_serializer(away_team_summary, many=True).data

        data = {
            match.home_team.name: home_team_summary_data,
            match.away_team.name: away_team_summary_data,
        }

        return Response(data, status=status.HTTP_200_OK)
