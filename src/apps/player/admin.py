from django.contrib import admin

from player.models import Player, Statistics, LineUp


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('surname', 'team')
    search_fields = ('surname', 'team')


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    ...


class MatchLineupInline(admin.TabularInline):
    model = LineUp
    extra = 1
    autocomplete_fields = ['player']
