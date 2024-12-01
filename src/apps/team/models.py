from django.db.models import UniqueConstraint

from core.django_model.mixins import CreatedUpdatedAt, UuidPk
from django.db import models

from user.models import UserProfile


class Tournament(CreatedUpdatedAt):
    name = models.CharField(max_length=255, unique=True)
    code_name = models.CharField(primary_key=True, max_length=255, unique=True)
    ordering = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Team(CreatedUpdatedAt):
    name = models.CharField(max_length=255, unique=True)
    code_name = models.CharField(primary_key=True, max_length=255, unique=True)
    played = models.PositiveSmallIntegerField(default=0)
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    draws = models.PositiveSmallIntegerField(default=0)
    goals_for = models.PositiveSmallIntegerField(default=0)
    goals_against = models.PositiveSmallIntegerField(default=0)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['tournament', 'name'], name='tournament_unique_team_name')
        ]

    def __str__(self):
        return self.name


class Match(CreatedUpdatedAt, UuidPk):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_teams')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_teams')
    home_team_goals = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    away_team_goals = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    start_time = models.DateTimeField()
    full_time = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.start_time}: {self.home_team} - {self.away_team}'


class MatchEvent(CreatedUpdatedAt, UuidPk):
    from player.models import Player

    class ActionType(models.TextChoices):
        GOAL = 'goal', 'GOAL'
        YELLOW_CARD = 'yellow_card', 'YELLOW CARD'
        RED_CARD = 'red_card', 'RED CARD'
        SUB = 'sub', 'SUB'

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='events')
    minute = models.PositiveSmallIntegerField()
    action = models.CharField(choices=ActionType.choices, max_length=15)
    major_event_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='+')
    minor_event_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='+', null=True, blank=True)


class Poll(CreatedUpdatedAt, UuidPk):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='polls')


class Voice(CreatedUpdatedAt, UuidPk):
    class ChoiceType(models.TextChoices):
        HOME_WIN = 'home_win', 'HOME_WIN'
        AWAY_WIN = 'away_win', 'AWAY_WIN'
        DRAW = 'draw', 'DRAW'

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='voices')
    choice = models.CharField(max_length=8, choices=ChoiceType.choices)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='voices')

    class Meta:
        constraints = [UniqueConstraint(fields=['poll', 'profile'], name='poll_unique_profile')]
