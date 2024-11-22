from django_filters import FilterSet

from player.models import Player


class PlayerFilter(FilterSet):
    class Meta:
        model = Player
        fields = ['team']
