from django.db import models

from core.django_model.mixins import CreatedUpdatedAt, UuidPk
from user.models import User

__all__ = (
    'UserProfile',
)


class UserProfile(CreatedUpdatedAt, UuidPk):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

