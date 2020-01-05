"""Course models"""
from django.db import models

# My models
from players.models import Player


class Course(models.Model):
    title = models.CharField(max_length=70, blank=True, null=True, default="No Title")
    category = models.CharField(max_length=100, blank=True, null=True, default="Any")
    teacher = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return "%s by %s" % (self.title, self.teache.__str__())


class Module(models.Model):
    title = models.CharField(max_length=100, blank=False, null=True)
    level = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return "Module %s" % (self.title)


class Lesson(models.Model):
    title = models.CharField(max_length=70, blank=True, null=True)
    url = models.CharField(max_length=22, blank=False, null=True)
    description = models.TextField(null=True, blank=True)

    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "Lesson %s" % (self.title)


class Project(models.Model):
    title = models.CharField(max_length=70, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(null=True, upload_to = 'projects/')

    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "Project %s" % self.title


class Commentary(models.Model):
    body = models.TextField(null=True, blank=False)
    likes = models.IntegerField(null=False, blank=False, default=0)
    date = models.DateTimeField(auto_now_add=True)
    is_question = models.BooleanField(null=False, blank=False, default=False)

    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"Commentary with {self.likes} likes published on {self.date}"


class Answer(models.Model):
    body = models.TextField(null=True, blank=False)
    likes = models.IntegerField(null=False, blank=False, default=0)
    date = models.DateTimeField(auto_now_add=True)

    commentary_id = models.ForeignKey(Commentary, on_delete=models.CASCADE)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer published on {self.date}"