from django.contrib import admin

# Course Models
from .models import Course, Project, Lesson, Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'category', 'teacher']
    list_display_links = ['pk', 'title']
    list_editable = ['category', 'teacher']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'description', 'image', 'course']
    list_display_link = ['pk', 'title']
    list_editable = ['description', 'image']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'url']
    list_display_link = ['pk', 'title']
    list_editable = ['url']