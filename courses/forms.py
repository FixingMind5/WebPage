from django.forms import ModelForm

from .models import Course, Module, Project, Lesson, Commentary, Answer

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'category',
            'teacher'
        ]


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 
            'description',
            'photo'
        ]


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