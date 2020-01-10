from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms import ValidationError

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
    title = forms.CharField(max_length=70, required=True)
    description = forms.CharField(required=True)
    image = forms.ImageField(required=True)
    course = forms.CharField(max_length=15, required=True)

    class Meta:
        model = Project
        fields = [
            'title', 
            'description',
            'image',
            'course',
        ]
    
    def clean_course(self):
        try:
            course = Course.objects.get(abreviation=self.cleaned_data.get("course"))
        except Course.DoesNotExist:
            raise ValidationError("El curso no existe 🚗")
        return course

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        return cleaned_data


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'title',
            'url',
            'description'
        ]


class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = [
            'title',
            'level'
        ]