from core.base_command import BaseCommand
from player.models import Player
from player.services.statistics_manager import StatisticsManager


class Command(BaseCommand):
    help = 'Generate default stats for players'

    def handle(self, *args, **options):
        players = Player.objects.filter(statistics__isnull=True)
        StatisticsManager.make_default_statistics(players)
