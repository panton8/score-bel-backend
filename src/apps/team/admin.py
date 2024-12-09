from django.contrib import admin

from player.admin import MatchLineupInline
from player.models import Player
from team.models import Team, Tournament, Match, MatchEvent


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    ...


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    ...


class MatchEventInline(admin.TabularInline):
    model = MatchEvent
    extra = 0
    fields = ('minute', 'action', 'major_event_player', 'minor_event_player')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ['major_event_player', 'minor_event_player']:
            match_id = request.resolver_match.kwargs.get('object_id')
            match = Match.objects.get(pk=match_id)
            kwargs["queryset"] = Player.objects.filter(team__in=[match.home_team, match.away_team])

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    fields = ('home_team', 'away_team', 'home_team_goals', 'away_team_goals', 'start_time', 'full_time', 'tournament')
    list_display = ('home_team', 'away_team', 'start_time', 'full_time')
    inlines = [MatchLineupInline, MatchEventInline]


