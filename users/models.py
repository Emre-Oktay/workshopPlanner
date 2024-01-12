from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('participant', 'Participant'),
        ('creator', 'Creator'),
    ]

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='participant',
    )

    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        null=True, default="avatar.svg")

    def __str__(self) -> str:
        return self.username
