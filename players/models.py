from django.contrib.auth.models import User
from django.db import models

# Utilities

# My models


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    birth_date = models.DateField()
    description = models.CharField(max_length=140, blank=True, null=True)
    image = models.ImageField(null=True, upload_to="player_profile_images/", default="default_user.png")
    facebook = models.CharField(blank=True, null=True, max_length=200)
    twitter = models.CharField(blank=True, null=True, max_length=200)
    instagram = models.CharField(blank=True, null=True, max_length=200)
    youtube = models.CharField(blank=True, null=True, max_length=200)
    website = models.CharField(blank=True, null=True, max_length=50)

    points = models.IntegerField(default=0, null=True)

    # Game Logic
    cluster = models.CharField(max_length=30, default='Starter')
    grade = models.CharField(max_length=40, default="Thinker")

    def __str__(self):
        return self.user.username
