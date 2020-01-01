from django.contrib.auth.models import User
from django.db import models

# Utilities

# My models from achievements

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    birth_date = models.DateField()
    description = models.CharField(max_length=140, blank=True, null=True)
    image = models.ImageField(null=True, upload_to="player/player_profile_images")
    facebook = models.CharField(blank=True, null=True, max_length=200)
    twitter = models.CharField(blank=True, null=True, max_length=200)
    instagram = models.CharField(blank=True, null=True, max_length=200)
    youtube = models.CharField(blank=True, null=True, max_length=200)
    website = models.CharField(blank=True, null=True, max_length=50)

    age = models.IntegerField()
    points = models.IntegerField(default=0, null=True)

    # Game Logic
    cluster = models.CharField(max_length=30)
    grade = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username
