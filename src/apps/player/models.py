from django.db import models
from django.db.models import UniqueConstraint

from core.django_model.mixins import CreatedUpdatedAt, UuidPk
from team.models import Team, Match


class Player(CreatedUpdatedAt, UuidPk):
    class Position(models.TextChoices):
        GOALKEEPER = 'gkp', 'GKP'
        DEFENDER = 'def', 'DEF'
        MIDFIELDER = 'mid', 'MID'
        FORWARD = 'fwd', 'FWD'

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    birth_date = models.DateField()
    position = models.CharField(choices=Position.choices, max_length=3)
    player_number = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['team', 'player_number'], name='team_unique_player_number')
        ]

    def __str__(self):
        return f'{self.name} {self.surname} - {self.team}'


class Statistics(CreatedUpdatedAt, UuidPk):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='statistics')
    goals = models.PositiveSmallIntegerField(default=0)
    assists = models.PositiveSmallIntegerField(default=0)
    clean_sheets = models.PositiveSmallIntegerField(default=0)
    yellow_cards = models.PositiveSmallIntegerField(default=0)
    red_cards = models.PositiveSmallIntegerField(default=0)


class LineUp(CreatedUpdatedAt, UuidPk):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='line_up')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='appearances')
    in_start = models.BooleanField(default=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['match', 'player'], name='match_unique_player')
        ]
