"""Course models"""
from django.db import models
from django.contrib.auth.models import User

# My models
from players.models import Player


class Project(models.Model):
    title = models.CharField(max_length=70, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, upload_to='projects/')

    def __str__(self):
        return "Project %s" % self.title


class Course(models.Model):
    title = models.CharField(max_length=70, blank=True, null=True, default="No Title")
    category = models.CharField(max_length=100, blank=True, null=True, default="Any")
    abreviation = models.CharField(max_length=15, blank=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return "%s by %s" % (self.title, self.teacher.__str__())


class Module(models.Model):
    title = models.CharField(max_length=100, blank=False, null=True)
    level = models.CharField(max_length=15, blank=True, null=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "Module %s" % (self.title)


class Lesson(models.Model):
    title = models.CharField(max_length=70, blank=False, null=True)
    url = models.CharField(max_length=22, blank=False, null=True)
    description = models.TextField(null=True, blank=True)
    views = models.IntegerField(blank=False, null=False, default=0)

    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "Lesson %s" % (self.title)


class Comentary(models.Model):
    text = models.TextField(null=False, blank=False, default='No text')
    likes = models.IntegerField(null=False, blank=False, default=0)
    date = models.DateTimeField(auto_now_add=True)
    is_question = models.BooleanField(null=False, blank=False, default=False)

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"Commentary with {self.likes} likes published on {self.date}"


class Answer(models.Model):
    text = models.TextField(null=False, blank=False)
    likes = models.IntegerField(null=False, blank=False, default=0)
    date = models.DateTimeField(auto_now_add=True)

    commentary = models.ForeignKey(Comentary, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer published on {self.date}"