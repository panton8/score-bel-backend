import factory

from django.test import TestCase

from team.services.team_manager import TeamManager
from team.testing.factories import TeamFactory, TournamentFactory


class TestCardProviderHider(TestCase):
    def setUp(self):
        self.service = TeamManager()

    def test_team_manager__make_tournament_table__correct_res(self):
        tournament = TournamentFactory.create()
        TeamFactory.create_batch(
            5,
            code_name=factory.Iterator(['neman', 'bate', 'arsenal', 'torpedo', 'dnepr']),
            played=factory.Iterator([12, 12, 12, 11, 12]),
            wins=factory.Iterator([8, 9, 6, 6, 3]),
            losses=factory.Iterator([1, 3, 6, 5, 9]),
            draws=factory.Iterator([3, 0, 0, 0, 0]),
            goals_for=factory.Iterator([30, 25, 13, 13, 10]),
            goals_against=factory.Iterator([17, 24, 13, 13, 36]),
            tournament=tournament,
        )
        res = self.service.get_actual_tournament_table(tournament)
        teams_codes = list(res.values_list('code_name', flat=True))
        self.assertEqual(teams_codes, ['bate', 'neman', 'torpedo', 'arsenal', 'dnepr'])
