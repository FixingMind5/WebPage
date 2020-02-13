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
from .models import Course, Module, Project, Lesson, Commentary, Answer


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
