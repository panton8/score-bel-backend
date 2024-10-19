from django.contrib.auth.password_validation import validate_password
from django.db.transaction import atomic
from rest_framework import serializers

from user.models import UserProfile, User


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    @atomic
    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        user = User.objects.create(username=username, email=email)

        user.set_password(validated_data.get('password'))
        user.save()

        profile = UserProfile.objects.create(user=user)
        return profile
