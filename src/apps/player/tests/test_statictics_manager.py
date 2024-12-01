from django.test import TestCase

from player.models import Statistics
from player.services.statistics_manager import StatisticsManager
from player.testing.factories import PlayerFactory, StatisticsFactory


class TestStatisticsManager(TestCase):
    def setUp(self):
        self.player = PlayerFactory()
        self.manager = StatisticsManager(player=self.player)

    def test_stat_manager__default_stats__ok(self):
        players = PlayerFactory.create_batch(5)
        stats_before_count = Statistics.objects.filter(player_id__in=[player.pk for player in players]).count()
        StatisticsManager.make_default_statistics(players)
        stats_after = Statistics.objects.filter(player_id__in=[player.pk for player in players])

        self.assertEqual(stats_before_count, 0)
        self.assertEqual(stats_after.count(), 5)

        for stat in stats_after:
            self.assertEqual(stat.goals, 0)
            self.assertEqual(stat.assists, 0)
            self.assertEqual(stat.clean_sheets, 0)
            self.assertEqual(stat.yellow_cards, 0)
            self.assertEqual(stat.red_cards, 0)

    def test_stat_manager__player_stats__ok(self):
        stat = StatisticsFactory(player=self.player)
        res = self.manager.get_statistics()

        self.assertEqual(res.player, self.player)
        self.assertEqual(res.goals, stat.goals,)
        self.assertEqual(res.assists, stat.assists)
        self.assertEqual(res.yellow_cards, stat.yellow_cards)
        self.assertEqual(res.red_cards, stat.red_cards)
        self.assertEqual(res.clean_sheets, stat.clean_sheets)
