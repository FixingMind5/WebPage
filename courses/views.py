# Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import QueryDict
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

# Forms builded
from courses.forms import CourseForm, ProjectForm, LessonForm, ModuleForm

# My models
from .models import Project


@login_required
def add_course(request):
    return render(
        request=request, 
        template_name='courses/add_course.html', 
    )


class CreateCourseView(LoginRequiredMixin, CreateView):
    template_name = "courses/add_course.html"
    success_url = reverse_lazy("courses:add_course")
    form_class = CourseForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['user'] = self.request.user
        context_data['player'] = self.request.user.player
    
        return context_data


class CreateProjectView(LoginRequiredMixin, CreateView):
    template_name = "courses/add_course.html"
    success_url = reverse_lazy("courses:add_course")
    form_class = ProjectForm
    model = Project

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['user'] = self.request.user.player
        context_data['player'] = self.request.user.player
        return context_data

    






