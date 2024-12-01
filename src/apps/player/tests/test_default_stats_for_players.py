from django.core.management import call_command
import factory
from django.test import TestCase

from player.models import Statistics
from player.testing.factories import PlayerFactory, StatisticsFactory


class TestMakeDefaultStatForAllPlayers(TestCase):
    def setUp(self):
        self.command = 'default_stats_for_players'
        self.players = PlayerFactory.create_batch(5)

    def test_command__no_players_with_stats__ok(self):
        stats_before = Statistics.objects.count()
        call_command(self.command)
        stats_after = Statistics.objects.count()
        self.assertEqual(stats_before, 0)
        self.assertEqual(stats_after, 5)

    def test_command__some_players_with_stats__ok(self):
        StatisticsFactory.create_batch(3, player=factory.Iterator([self.players[0], self.players[1], self.players[2]]))
        stats_before = Statistics.objects.count()
        call_command(self.command)
        stats_after = Statistics.objects.count()
        self.assertEqual(stats_before, 3)
        self.assertEqual(stats_after, 5)
