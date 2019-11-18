from django.contrib.auth.models import User
from django.db import models
from achievements.models import Medal, Pin, Degree

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField()
    points = models.IntegerField()

    # Game Logic
    cluster = models.CharField(max_length=30)
    grade = models.CharField(max_length=40)

    # Foreign Keys
    medal = models.ForeignKey(
        'achievements.Medal',
        on_delete=models.CASCADE,
        null = True
    )

    pin = models.ForeignKey(
        'achievements.Pin',
        on_delete = models.CASCADE,
        null = True
    )

    degree = models.ForeignKey(
        'achievements.Degree',
        on_delete = models.CASCADE,
        null = True
    )

    def __str__(self):
        return self.user.username
