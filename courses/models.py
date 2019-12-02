"""Course models"""
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=50)
    admissionProfile = models.CharField(max_length=200)
    dischargeProfile = models.CharField(max_length=200)
    schedules = models.CharField(max_length=100)
    courseLength = models.IntegerField()
    courseDescription = models.CharField(max_length=500)
    courseDocument = models.FileField(upload_to="temaries/", blank=True)
    courseBuilder = models.CharField(max_length=50, blank=True, null=True)
    courseCategory = models.CharField(max_length=60, blank=True)