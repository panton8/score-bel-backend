from rest_framework import serializers

from player.models import Player, Statistics, LineUp


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

    class Meta:
        model = Player
        exclude = ('id', 'name', 'birth_date', 'created_at', 'updated_at', 'team')


class LineUpSerializer(serializers.ModelSerializer):
    player = PlayerLineUpSerializer()

    class Meta:
        model = LineUp
        fields = ('player', )
