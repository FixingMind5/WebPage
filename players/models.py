from django.contrib.auth.models import User
from django.db import models

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField()
    points = models.IntegerField()

    # Game Logic
    cluster = models.CharField(max_length=30)
    grade = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username
