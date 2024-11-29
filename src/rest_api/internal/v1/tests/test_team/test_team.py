import factory
from datetime import datetime, date
from rest_framework.test import APIClient

from player.testing.factories import PlayerFactory, LineUpFactory
from rest_api.testing.api_test_case import ApiTestCase
from rest_api.testing.entity_test_api import EntityTestApi
from team.testing.factories import TeamFactory, TournamentFactory, MatchFactory


class TournamentTestApi(EntityTestApi):
    entity = 'internal_api:v1:tournaments'


class TournamentTestCase(ApiTestCase):

    def setUp(self):
        self.client = APIClient()
        self.api = TournamentTestApi(self.client)

    def test_tournament_list__ok(self):
        TournamentFactory.create_batch(3)

        rsp = self.api.get_entities()

        self.assertEqual(len(rsp), 3)

    def test_tournament_table__correct_data__no_data(self):
        tournament = TournamentFactory()
        TeamFactory.create_batch(
            3,
            code_name=factory.Iterator(['neman', 'bate', 'dnepr']),
            played=factory.Iterator([12, 12, 12]),
            wins=factory.Iterator([9, 8, 10]),
            losses=factory.Iterator([3, 4, 2]),
            draws=factory.Iterator([0, 0, 0]),
            goals_for=factory.Iterator([30]),
            tournament=tournament,
        )

        rsp = self.api.detail_get_action('table', tournament.pk)

        self.assertEqual(rsp[0]['code_name'], 'dnepr')
        self.assertEqual(rsp[1]['code_name'], 'neman')
        self.assertEqual(rsp[2]['code_name'], 'bate')


class TeamTestApi(EntityTestApi):
    entity = 'internal_api:v1:teams'


class TeamTestCase(ApiTestCase):

    def setUp(self):
        self.client = APIClient()
        self.api = TeamTestApi(self.client)

    def test_team_list__ok(self):
        TeamFactory.create_batch(3)

        rsp = self.api.get_entities()

        self.assertEqual(len(rsp), 3)


class MatchTestApi(EntityTestApi):
    entity = 'internal_api:v1:matches'


class MatchTestCase(ApiTestCase):

    def setUp(self):
        self.client = APIClient()
        self.api = MatchTestApi(self.client)

    def test_match_list__ok(self):
        MatchFactory.create_batch(3)

        rsp = self.api.get_entities()

        self.assertEqual(len(rsp), 3)

    def test_match_list__date_filter__ok(self):
        dates = [datetime(2024, 11, 12, 21,0),
                 datetime(2024, 11, 12, 21, 1),
                 datetime(2024, 11, 11, 21, 0),
                 datetime(2024, 11, 11, 20, 59),
                 datetime(2024, 11, 12, 15, 0)]
        matches = MatchFactory.create_batch(5, start_time=factory.Iterator(dates), tournament=TournamentFactory())

        rsp = self.api.get_entities(filters={'date': date(2024, 11, 12)})

        self.assertEqual(len(rsp), 3)
        self.assertEqual(rsp[0]['id'], str(matches[2].id))
        self.assertEqual(rsp[1]['id'], str(matches[4].id))
        self.assertEqual(rsp[2]['id'], str(matches[0].id))

    def test_match_list__tournament_filter__ok(self):
        tournaments = TournamentFactory.create_batch(3)
        MatchFactory.create_batch(4, tournament=factory.Iterator([tournaments[0], tournaments[1], tournaments[2], tournaments[1]]))

        rsp = self.api.get_entities(filters={'tournament': tournaments[1].pk})

        self.assertEqual(len(rsp), 2)
        for match in rsp:
            self.assertEqual(match['tournament'], str(tournaments[1].pk))

    def test_match_list__full_time_filter__ok(self):
        MatchFactory.create_batch(5, full_time=factory.Iterator([True, True, False, True, False]))

        rsp = self.api.get_entities(filters={'full_time': True})

        self.assertEqual(len(rsp), 3)
        for match in rsp:
            self.assertTrue(match['full_time'])

    def test_match_line_up__ok(self):
        teams = TeamFactory.create_batch(2)
        match = MatchFactory(home_team=teams[0], away_team=teams[1])
        players = PlayerFactory.create_batch(
            4,
            team=factory.Iterator([teams[0], teams[0], teams[1], teams[1]]),
            surname=factory.Iterator(['A', 'C', 'F', 'G']),
            player_number=factory.Iterator([10, 11, 12, 13])
        )
        LineUpFactory.create_batch(4, match=match, player=factory.Iterator(players), in_start=factory.Iterator([True, True, False, True]))
        rsp = self.api.detail_get_action('line-up', match.pk)
        self.assertEqual(len(rsp), 2)
        self.assertIsNotNone(rsp[match.home_team.name])
        self.assertIsNotNone(rsp[match.away_team.name])

    def test_match_summary__ok(self):
        teams = TeamFactory.create_batch(2)
        match = MatchFactory(home_team=teams[0], away_team=teams[1])
        players = PlayerFactory.create_batch(
            4,
            team=factory.Iterator([teams[0], teams[0], teams[1], teams[1]]),
            surname=factory.Iterator(['A', 'C', 'F', 'G']),
            player_number=factory.Iterator([10, 11, 12, 13])
        )

