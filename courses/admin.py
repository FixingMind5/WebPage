from django.contrib import admin

# Course Models
from courses.models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass