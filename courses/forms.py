from django import forms

from courses.models import Course

class CourseModel(forms.Form):
    course_title = forms.CharField(max_length=70, required=True)
    teacher = forms.CharField(max_length=50, required=True)
    category = forms.CharField(max_length=100, required=True)


class ProjectModel(forms.Form):
    project_title = forms.CharField(max_length=70, required=True)
    description = forms.CharField(required=True)
    image = forms.ImageField(required=True)


class LessonModel(forms.Form):
    lesson_title = forms.CharField(max_length=70, required=True)
    url = forms.CharField(max_length=22, required=True)
    # description = forms.CharField(required=True)


class ModuleModel(forms.Form):
    module_title = forms.CharField(max_length=100, required=True)
    level = forms.CharField(max_length=15, required=True)