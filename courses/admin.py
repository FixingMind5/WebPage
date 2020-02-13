from django.contrib import admin

# Course Models
from .models import Course, Project, Lesson, Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'category', 'teacher', 'project']
    list_display_links = ['pk', 'title']
    list_editable = ['category', 'teacher']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'description', 'image',]
    list_display_link = ['pk', 'title']
    list_editable = ['description', 'image']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'level', 'course']
    list_display_link = ['pk', 'title']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'url', 'module', 'course']
    list_display_link = ['pk', 'title']
    list_editable = ['url']