import factory
from datetime import datetime, date
from rest_framework.test import APIClient
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED

from player.models import Player
from player.testing.factories import PlayerFactory, LineUpFactory, MatchEventFactory, StatisticsFactory
from rest_api.testing.api_test_case import ApiTestCase
from rest_api.testing.entity_test_api import EntityTestApi
from team.models import MatchEvent
from team.testing.factories import TeamFactory, TournamentFactory, MatchFactory, PollFactory, VoiceFactory
from user.testing.factories import UserProfileFactory


class PlayerTestApi(EntityTestApi):
    entity = 'internal_api:v1:players'


class PLayerTestCase(ApiTestCase):

    def setUp(self):
        self.client = APIClient()
        self.api = PlayerTestApi(self.client)
        self.players = PlayerFactory.create_batch(3)

    def test_player_statistics__ok(self):
        stats = StatisticsFactory.create_batch(
            3,
            player=factory.Iterator(self.players),
            goals=factory.Iterator([1, 2, 3]),
            assists=factory.Iterator([5, 6, 7]),
            clean_sheets=factory.Iterator([8, 9, 10]),
            yellow_cards=factory.Iterator([0, 1, 2]),
            red_cards=factory.Iterator([0, 3, 1]),
        )

        rsp = self.api.detail_get_action('statistics', self.players[0].pk)

        self.assertEqual(rsp['goals'], stats[0].goals)
        self.assertEqual(rsp['assists'], stats[0].assists)
        self.assertEqual(rsp['clean_sheets'], stats[0].clean_sheets)
        self.assertEqual(rsp['yellow_cards'], stats[0].yellow_cards)
        self.assertEqual(rsp['red_cards'], stats[0].red_cards)

    def test_player_list__ok(self):
        rsp = self.api.get_entities()
        self.assertEqual(len(rsp), 3)

    def test_player_list_by_team__ok(self):
        team = TeamFactory()
        PlayerFactory.create_batch(2, team=team, player_number=factory.Iterator([99, 12]))
        players = Player.objects.count()
        rsp = self.api.get_entities(filters={'team': team.pk})
        self.assertEqual(len(rsp), 2)
        self.assertEqual(players, 5)

