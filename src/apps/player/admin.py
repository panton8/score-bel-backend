from django.contrib import admin
from django.forms import ModelForm

from player.models import Player, Statistics, LineUp
from team.models import Match


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('surname', 'team')
    search_fields = ('surname', 'team')


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    ...


class MatchLineupInline(admin.TabularInline):
    model = LineUp
    extra = 0
    fields = ('player', 'in_start', )
    ordering = ('player__team', 'player__position')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'player':
            match_id = request.resolver_match.kwargs.get('object_id')
            match = Match.objects.get(pk=match_id)
            kwargs['queryset'] = Player.objects.filter(team__in=[match.home_team, match.away_team])

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
