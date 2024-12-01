import factory
from datetime import datetime

from team.models import Tournament, Team, Match, Poll, Voice
from user.testing.factories import UserProfileFactory


class TournamentFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    code_name = factory.Faker('uuid4')
    ordering = 1

    class Meta:
        model = Tournament


class TeamFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    code_name = factory.Faker('uuid4')
    played = 12
    wins = 9
    losses = 2
    draws = 1
    goals_for = 30
    goals_against = 17
    tournament = factory.SubFactory(TournamentFactory)

    class Meta:
        model = Team


class MatchFactory(factory.django.DjangoModelFactory):
    tournament = factory.SubFactory(TournamentFactory)
    home_team = factory.SubFactory(TeamFactory)
    away_team = factory.SubFactory(TeamFactory)
    home_team_goals = None
    away_team_goals = None
    start_time = datetime(2024, 11, 15, 16, 30)
    full_time = False
    processed = False

    class Meta:
        model = Match


class PollFactory(factory.django.DjangoModelFactory):
    match = factory.SubFactory(MatchFactory)

    class Meta:
        model = Poll


class VoiceFactory(factory.django.DjangoModelFactory):
    poll = factory.SubFactory(PollFactory)
    profile = factory.SubFactory(UserProfileFactory)
    choice = Voice.ChoiceType.HOME_WIN

    class Meta:
        model = Voice
