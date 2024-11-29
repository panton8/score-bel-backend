import factory
from datetime import date

from player.models import Player, Statistics, LineUp
from team.models import MatchEvent
from team.testing.factories import TeamFactory, MatchFactory


class PlayerFactory(factory.django.DjangoModelFactory):
    name = 'Eden'
    surname = 'Hazard'
    team = factory.SubFactory(TeamFactory)
    birth_date = date(1987, 1, 7)
    position = Player.Position.MIDFIELDER
    player_number = 10

    class Meta:
        model = Player


class StatisticsFactory(factory.django.DjangoModelFactory):
    player = factory.SubFactory(PlayerFactory)
    goals = 12
    assists = 4
    clean_sheets = 6
    yellow_cards = 4
    red_cards = 0

    class Meta:
        model = Statistics


class LineUpFactory(factory.django.DjangoModelFactory):
    match = factory.SubFactory(MatchFactory)
    player = factory.SubFactory(PlayerFactory)
    in_start = True

    class Meta:
        model = LineUp


class MatchEventFactory(factory.django.DjangoModelFactory):
    match = factory.SubFactory(MatchFactory)
    minute = 85
    action = MatchEvent.ActionType.GOAL
    major_event_player = factory.SubFactory(PlayerFactory)
    minor_event_player = factory.SubFactory(PlayerFactory)

    class Meta:
        model = MatchEvent
