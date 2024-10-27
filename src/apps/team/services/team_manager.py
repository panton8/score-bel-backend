from team.models import Team, Tournament


class TeamManager:
    def get_actual_tournament_table(self, tournament: Tournament):
        table = Team.objects.filter(tournament=tournament)\
            .order_by('-wins', '-draws', '-goals_for', 'goals_against', 'played')
        return table
