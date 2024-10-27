import factory
from datetime import datetime, date
from rest_framework.test import APIClient

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