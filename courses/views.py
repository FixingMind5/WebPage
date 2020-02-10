# Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import QueryDict
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import ValidationError
from django.http import HttpResponse

# Forms builded
from courses.forms import CourseForm, ModuleForm, ProjectForm, LessonFormSet

# My models
from .models import Project, Module, Course, Lesson


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
                # Pendiente: Crear una vista bonita de logrado
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

@login_required
def add_lesson(request):
    template_name = 'courses/add_lesson.html'
    if request.method == 'GET':
        lesson_formset = LessonFormSet(queryset=Module.objects.none())
        form = ModuleForm(request.GET or None)
    elif request.method == 'POST':
        form = ModuleForm(request.POST)
        lesson_formset = LessonFormSet(request.POST)
        if form.is_valid() and lesson_formset.is_valid():
            module = form.save()
            for form in lesson_formset:
                lesson = form.save(commit=False)
                lesson.module = module
                lesson.course = module.course
                lesson.save()
            return redirect('courses:add_lesson')
    return render(
        request=request,
        template_name=template_name,
        context={
            'form': form,
            'lesson_formset': lesson_formset
        }
    )
 

class CourseCatalogView(ListView):
    template_name = 'courses/course_catalog.html'
    model = Course
    queryset = Course.objects.all()


class AdminCourseView(LoginRequiredMixin, DetailView):
    template_name = 'courses/admin_course_detail.html'