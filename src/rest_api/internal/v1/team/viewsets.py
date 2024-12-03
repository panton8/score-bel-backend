from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_api.internal.v1.player.serializers import LineUpSerializer, SummarySerializer, VoteSerializer, \
    DiscussionMessageSerializer
from rest_api.internal.v1.team.serializers import TeamSerializer, TournamentSerializer, MatchSerializer
from team.filters import MatchFilter
from team.models import Team, Tournament, Match, Voice
from rest_framework.permissions import AllowAny, IsAuthenticated

from team.services.discussion_service import DiscussionService
from team.services.line_up_manager import LineUpManager
from team.services.poll_service import PollService
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

    @action(detail=True, methods=['GET'], permission_classes=(AllowAny,))
    def poll(self, request, *args, **kwargs):
        match = self.get_object()

        poll_res = PollService().get_poll_result(match=match)
        return Response(data=poll_res, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], serializer_class=VoteSerializer, permission_classes=(IsAuthenticated,))
    def vote(self, request, *args, **kwargs):
        match = self.get_object()
        profile = request.user.profile
        poll_service = PollService()

        profile_voice = poll_service.is_profile_voted(profile=profile, match=match)

        if profile_voice:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        poll_service.make_voice(profile, match, data['choice'])
        poll_res = poll_service.get_poll_result(match)
        data = {
            'profile_voice': data['choice'],
            'poll_results': poll_res
        }

        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET'], permission_classes=(AllowAny,),
            serializer_class=DiscussionMessageSerializer, url_path='discussion-messages')
    def discussion_messages(self, request, *args, **kwargs):
        match = self.get_object()
        discussion_service = DiscussionService()
        discussion = discussion_service.get_discussion(match)
        messages = discussion_service.get_discussions_messages(discussion)

        messages_data = self.get_serializer(messages, many=True).data

        return Response(messages_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=(IsAuthenticated,),
            serializer_class=DiscussionMessageSerializer, url_path='message')
    def message(self, request, *args, **kwargs):
        match = self.get_object()
        profile = request.user.profile
        discussion_service = DiscussionService()
        discussion = discussion_service.get_discussion(match)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        msg = serializer.validated_data['message']
        discussion_service.add_message_to_discussion(profile, discussion, msg)

        return Response(data={'message': msg}, status=status.HTTP_201_CREATED)

