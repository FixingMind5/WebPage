# Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import QueryDict

# Forms builded
from courses.forms import CourseModel, ProjectModel, LessonModel, ModuleModel

# Utilities
import csv


@login_required
def add_course(request):
    category_course_dictionary = {
        1: "Programación",
        2: "Matemáticas",
        3: "Diseño"
    }
    return render(request, 'courses/add_course.html', { "categories": category_course_dictionary})


@login_required
def upload_course(request):
    """Register a course form a csv, pdf and photo file"""
    if request.method == 'POST':
        pass




