from django.contrib import admin

from player.admin import MatchLineupInline
from team.models import Team, Tournament, Match


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    ...


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    ...


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    fields = ('home_team', 'away_team', 'home_team_goals', 'away_team_goals', 'start_time', 'full_time', 'tournament')
    list_display = ('home_team', 'away_team', 'start_time', 'full_time')
    inlines = [MatchLineupInline]
