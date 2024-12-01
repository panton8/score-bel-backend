from player.models import Player, Statistics
from django.db.models import QuerySet


class StatisticsManager:
    def __init__(self, player: Player) -> None:
        self.player = player

    def get_statistics(self) -> Statistics:
        return Statistics.objects.get(player=self.player)

    @staticmethod
    def make_default_statistics(players: QuerySet[Player]) -> None:
        players_stats_to_create = []
        for player in players:
            players_stats_to_create.append(
                Statistics(player=player)
            )

        Statistics.objects.bulk_create(players_stats_to_create, ignore_conflicts=True)
