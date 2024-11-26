from team.models import Match, MatchEvent


class SummaryManager:
    def __init__(self, match: Match):
        self.match = match

    def get_home_team_summary(self):
        qs = MatchEvent.objects.filter(match=self.match, major_event_player__team=self.match.home_team)

        return qs.order_by('minute', 'created_at')

    def get_away_team_summary(self):
        qs = MatchEvent.objects.filter(match=self.match, major_event_player__team=self.match.away_team)

        return qs.order_by('minute', 'created_at')
