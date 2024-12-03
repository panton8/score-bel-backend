from rest_framework import serializers

from team.models import Tournament, Team, Match


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('code_name', 'name')


class TeamSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()
    goals_diff = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('code_name', 'name', 'played', 'wins', 'losses', 'draws', 'goals_for',
                  'goals_against', 'goals_diff', 'points', 'tournament', 'logo')

    def get_points(self, team: Team) -> int:
        return team.wins * 3 + team.draws

    def get_goals_diff(self, team: Team) -> int:
        return team.goals_for - team.goals_against


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'home_team', 'away_team', 'home_team_goals',
                  'away_team_goals', 'start_time', 'full_time', 'tournament')
