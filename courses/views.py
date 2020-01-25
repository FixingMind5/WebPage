# Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import QueryDict
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import ValidationError
from django.http import HttpResponse

# Forms builded
from courses.forms import CourseForm, ModuleFormSet, ProjectForm, LessonFormSet

# My models
from .models import Project, Module, Course


class CreateCourseView(LoginRequiredMixin, CreateView):
    template_name = "courses/add_course.html"
    success_url = reverse_lazy("courses:add_course")
    form_class = CourseForm

    def get_context_data(self, **kwargs):
        context_data = super(CreateCourseView, self).get_context_data(**kwargs)
        context_data['user'] = self.request.user
        context_data['player'] = self.request.user.player
    
        return context_data
    
    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        project_form = ProjectForm()
        return self.render_to_response(
            self.get_context_data(
                form=form,
                project_form=project_form,
            )
        )
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = CourseForm(self.request.POST)
        project_form = ProjectForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.save()
            if project_form.is_valid():
                project_form.save()
                return HttpResponse('Done!')
            else:
                return self.form_invalid(form, project_form)
        else:
            return self.form_invalid(form, project_form)

    def form_invalid(self, form, project_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                project_form=project_form
            )
        )


# class CreateProjectView(LoginRequiredMixin, CreateView):
#     template_name = "courses/add_course.html"
#     success_url = reverse_lazy("courses:add_course")
#     form_class = ProjectForm
#     model = Project

#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['user'] = self.request.user.player
#         context_data['player'] = self.request.user.player
#         return context_data


# class CreateModuleView(LoginRequiredMixin, CreateView):
#     template_name = "courses/add_course.html"
#     success_url = None
#     form_class = ModuleForm
#     model = Module

#     def get_context_data(self, **kwargs):
#         data = super(CreateModuleView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['lessons'] = LessonFormSet(self.request.POST)
#         else:
#             data['lessons'] = LessonFormSet()
#         return data

#     def form_valid(self, form):
#         context = self.get_context_data()
#         lessons = context['lessons']
#         with transaction.atomic():
#             form.instance.created_by = self.request.user
#             self.object = self.save()
#             if lessons.is_valid():
#                 lessons.instance = self.object
#                 lessons.save()
#         return super(CreateModuleView, self).form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy('courses:add_course')


# class CreateLessonView(LoginRequiredMixin, CreateView):
#     template_name = "courses/add_course.html"
#     success_url = reverse_lazy("courses:add_course")
#     form_class = LessonForm
