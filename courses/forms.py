from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms import ValidationError

# Utilities
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import Formset

# Django models
from django.forms.models import inlineformset_factory

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


class ProjectForm(ModelForm):
    description = forms.CharField(required=True)
    class Meta:
        model = Project
        exclude = ('course',)
    
    def save(self):
        old_data = self.data
        cleaned_data = self.cleaned_data
        course = Course.objects.get(title=old_data['title'])
        data = {
            'course': course,
            'title': old_data['project_title'],
            'description': old_data['description'],
            'image': cleaned_data['image']
        }
        project = Project.objects.create(**data)
        project.save()


class ModuleForm(ModelForm):
    class Meta:
        model = Module
        exclude = ()


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        exclude = ()

ProjectFormSet = inlineformset_factory(Course, Project, form=ProjectForm, fields=["title", "description", "image"], can_delete=False,extra=1)
ModuleFormSet = inlineformset_factory(Course, Module, fields=["title", "level"], form=ModuleForm, can_delete=True, extra=1)
LessonFormSet = inlineformset_factory(Course, Lesson, fields=['title', 'url'], form=LessonForm, can_delete=True, extra=1)
