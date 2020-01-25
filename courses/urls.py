# Django utilities
from django.urls import path

from courses import views

urlpatterns = [
    path(
        route='add_course/', 
        view=views.CreateCourseView.as_view(), 
        name="add_course"
    ),
]