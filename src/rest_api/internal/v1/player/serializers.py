from rest_framework import serializers

from player.models import Player, Statistics, LineUp
from team.models import MatchEvent, Voice
from typing import Optional


class PlayerSerializer(serializers.ModelSerializer):
    team = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'name', 'surname', 'team', 'birth_date', 'position', 'player_number')


class StatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statistics
        fields = ('goals', 'assists', 'clean_sheets', 'yellow_cards', 'red_cards')


class PlayerLineUpSerializer(PlayerSerializer):
    team = None
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ('id', 'display_name', 'position', 'player_number')

    def get_display_name(self, obj: Player) -> str:
        return f'{obj.name[0]}.{obj.surname}'


class LineUpSerializer(serializers.ModelSerializer):
    player = PlayerLineUpSerializer()

    class Meta:
        model = LineUp
        fields = ('player', )


class SummarySerializer(serializers.ModelSerializer):
    major_event_player_name = serializers.SerializerMethodField()
    minor_event_player_name = serializers.SerializerMethodField()

    class Meta:
        model = MatchEvent
        fields = ('minute', 'action', 'major_event_player_name', 'minor_event_player_name')

    def get_major_event_player_name(self, obj: MatchEvent) -> str:
        return f'{obj.major_event_player.name[0]}.{obj.major_event_player.surname}'

    def get_minor_event_player_name(self, obj: MatchEvent) -> Optional[str]:
        if not obj.minor_event_player:
            return None
        return f'{obj.minor_event_player.name[0]}.{obj.minor_event_player.surname}'


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Voice
        fields = ('choice', )
