from django.db.models import UniqueConstraint

from core.django_model.mixins import CreatedUpdatedAt, UuidPk
from django.db import models


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
