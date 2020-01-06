# Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import QueryDict
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Forms builded
from courses.forms import CourseForm, ProjectForm, LessonForm, ModuleForm


@login_required
def add_course(request):
    category_course_dictionary = {
        1: "Programación",
        2: "Matemáticas",
        3: "Diseño"
    }

    return render(
        request=request, 
        template_name='courses/add_course.html', 
        context={ 
            "categories": category_course_dictionary,
        },
    )


class CreateCourseView(LoginRequiredMixin, CreateView):
    pass






