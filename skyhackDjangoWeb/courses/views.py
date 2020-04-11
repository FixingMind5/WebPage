# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import QueryDict, Http404
from django.views.generic import CreateView, DetailView, ListView, FormView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import ValidationError
from django.http import HttpResponse

# Forms builded
from skyhackDjangoWeb.courses.forms import CourseForm, ModuleForm, ProjectForm, LessonFormSet, ComentaryForm, AnswerForm

# My models
from .models import Project, Module, Course, Lesson, Comentary, Answer


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
        if project_form.is_valid():
            project_form.save()
            if form.is_valid():
                form.save()
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
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context_data = super(CourseCatalogView, self).get_context_data(**kwargs)
        context_data['user'] = self.request.user

        return context_data


class CourseDetailView(LoginRequiredMixin, ListView):
    template_name = 'courses/course.html'
    slug_url_kwarg = 'abreviation'
    slug_field = 'abreviation'
    queryset = Course.objects.all()
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context_data = super(CourseDetailView, self).get_context_data(**kwargs)
        context_data['user'] = self.request.user
        context_data['project'] = context_data['object_list'][0].project
        context_data['teacher'] = context_data['object_list'][0].teacher
        course = context_data['object_list'][0]
        context_data['course'] = course
        context_data['modules'] = Module.objects.filter(course=course)
        context_data['lessons'] = Lesson.objects.filter(course=course)

        return context_data


class LessonDetaiView(LoginRequiredMixin, DetailView):
    template_name = 'courses/lesson.html'
    slug_url_kwarg = 'pk'
    slug_field = 'pk'
    queryset = Lesson.objects.all()
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context_data = super(LessonDetaiView, self).get_context_data(**kwargs)
        lesson = context_data['lesson']
        context_data["comentaries"] = Comentary.objects.filter(lesson=lesson)
        context_data['answers'] = Answer.objects.filter(lesson=lesson)

        return context_data


class AddComentaryView(LoginRequiredMixin, FormView):
    template_name = 'courses/lesson.html'
    form_class = ComentaryForm
    abreviation = None
    pk = None

    def post(self, request, *args, **kwargs):
        self.object = None
        form = ComentaryForm(self.request.POST)
        self.abreviation = self.request.POST['abreviation']
        self.pk = self.request.POST['pk']
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        url = reverse('courses:lesson', kwargs={'abreviation': self.abreviation, 'pk': self.pk})
        return redirect(url)

    def get_success_url(self):
        return reverse('courses:lesson', kwargs={'abreviation': self.abreviation, 'pk': self.pk}) 

class AddAnswerView(LoginRequiredMixin, FormView):
    template_name = 'courses/lesson.html'
    form_class = AnswerForm
    abreviation = None
    pk = None

    def post(self, request, *args, **kwargs):
        self.object = None
        form = AnswerForm(self.request.POST)
        self.abreviation = self.request.POST['abreviation']
        self.pk = self.request.POST['pk']
        print(form.errors)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        url = reverse('courses:lesson', kwargs={'abreviation': self.abreviation, 'pk': self.pk})
        return redirect(url)

    def get_success_url(self):
        return reverse('courses:lesson', kwargs={'abreviation': self.abreviation, 'pk': self.pk}) 

class AnswerDelete(LoginRequiredMixin, DeleteView):
    model = Answer
    abreviation = None
    lesson_pk = None

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Comentary, id=pk)

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        else:
            print(self.request.POST)
            self.abreviation = self.request.POST['abreviation']
            self.lesson_pk = self.request.POST['lesson_pk']
            url = reverse('courses:lesson', kwargs={'abreviation': self.abreviation, 'pk': self.lesson_pk})
            return url


class AdminCourseView(LoginRequiredMixin, DetailView):
    template_name = 'courses/admin_course_detail.html'