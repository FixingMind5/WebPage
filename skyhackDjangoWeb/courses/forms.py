from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms import ValidationError

# Utilities
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import Formset

# Django models
from django.forms.models import BaseModelFormSet
from django.forms import modelformset_factory

# My models
from .models import Course, Module, Project, Lesson, Comentary, Answer
from skyhackDjangoWeb.players.models import Player


class CourseForm(ModelForm):
    title = forms.CharField(max_length=70, required=True)
    teacher = forms.CharField(max_length=70, widget=forms.EmailInput(),required=True)
    category = forms.CharField(required=True)
    abreviation = forms.CharField(max_length=15, required=True)

    class Meta:
        model = Course
        fields = [
            'title',
            'abreviation',
            'category',
            'teacher',
        ]

    def clean_teacher(self):
        try:
            teacher = User.objects.get(email=self.cleaned_data.get('teacher'))
        except User.DoesNotExist:
            raise ValidationError("El usuario no existe 😢")
        return teacher

    def save(self):
        cleaned_data = self.cleaned_data
        project_title = self.data['project_title']
        print(self.data['project_title'])
        print(Project.objects.get(title=project_title))
        try:
            project = Project.objects.get(title=project_title)
        except Project.DoesNotExist:
            raise ValidationError("El proyecto no existe 😨")
        data = {
            'title': cleaned_data['title'],
            'abreviation': cleaned_data['abreviation'],
            'category': cleaned_data['category'],
            'teacher': cleaned_data['teacher'],
            'project': project
        }
        course = Course.objects.create(**data)
        course.save()


class ProjectForm(ModelForm):
    description = forms.CharField(required=True)
    class Meta:
        model = Project
        exclude = ('course',)
    
    def save(self):
        old_data = self.data
        cleaned_data = self.cleaned_data
        data = {
            'title': old_data['project_title'],
            'description': old_data['description'],
            'image': cleaned_data['image']
        }
        project = Project.objects.create(**data)
        project.save()


class ModuleForm(ModelForm):
    course = forms.CharField(max_length=70, required=True)
    class Meta:
        model = Module
        fields = (
            'course',
            'title',
            'level'
        )
        labels = {
            'title': 'Module Title'
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'título del módulo'
                }
            )
        }

    def clean_course(self):
        try:
            course = Course.objects.get(abreviation=self.data['course'])
        except Course.DoesNotExist:
            raise ValidationError(f"El curso con la abreviación {self.data['course']} no existe 💥")
        return course


class ComentaryForm(ModelForm):
    class Meta:
        model = Comentary
        fields = ("text",)
    
    def save(self):
        old_data = self.data
        is_question = True if 'is_question' in old_data else False
        lesson_pk = old_data['pk']
        lesson = Lesson.objects.get(pk=lesson_pk)
        username = old_data['player']
        user = User.objects.get(username=username)
        data = {
            'player': user.player,
            'lesson': lesson,
            'text': old_data['text'],
            'is_question': is_question,
        }
        comentary = Comentary.objects.create(**data)
        comentary.save()


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)

    def save(self):
        old_data = self.data
        pk = old_data['comentary_pk']
        comentary = Comentary.objects.get(pk=pk)
        username = old_data['username']
        lesson_pk = old_data['pk']
        lesson = Lesson.objects.get(pk=lesson_pk)
        user = User.objects.get(username=username)
        data = {
            'text': old_data['text'],
            'comentary': comentary,
            'player': user.player,
            'lesson': lesson
        }
        answer = Answer.objects.create(**data)
        answer.save()



LessonFormSet = modelformset_factory(
    Lesson,
    fields=('title', 'url'),
    extra=1,
    widgets={
        'title': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Título de la clase',
                'required': True
            }
        ),
        'url': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'YouTube url',
                'required': True
            }
        )
    },
)
