"""Models that creates the mold of medals, degrees and pins, essential
in the bussiness model, this things will represent the progress of our
players"""
from django.db import models

# Create your models here.

class Achievement(models.Model):
    title = models.CharField(max_length=40, default='No Title')
    points = models.IntegerField()
    description = models.CharField(max_length=100, default='No Description')
    image = models.ImageField(
        upload_to='achievements/images',
        blank = True,
        null = True
    )
    type = models.CharField(max_length=10)

    def __str__(self):
        return f"Medal named {self.title}"
