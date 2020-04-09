"""QRClothes models utils"""

# Django models
from django.db import models

class QRProduct(models.Model):
    """QRPRoduct Model.

    A QRProduct is a base Product with all
    characteristics such as name, alias, prize, color
    and other stats like fire points, hype and fires
    that describes presence of product in page.
    """
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    alias = models.CharField(max_length=15, blank=False, null=False, unique=True)
    prize = models.PositiveIntegerField(blank=False, null=False)
    creation_year = models.CharField(max_length=4)
    color = models.CharField(max_length=10)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    # Stats
    fire_points = models.PositiveIntegerField(blank=False, null=False)
    hype = models.PositiveIntegerField(blank=False, null=False, default=0)
    fires = models.FloatField(default=0)

    class Meta:
        abstract = True
        get_latest_by = 'hype'
        ordering = ['-hype', '-fires', '-fire_points']