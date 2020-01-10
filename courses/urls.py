# Django utilities
from django.urls import path

from courses import views

urlpatterns = [
    path(
        route='add_course/', 
        view=views.add_course, 
        name="add_course"
    ),
    path(
        route="submit_basic_information/",
        view=views.CreateCourseView.as_view(),
        name="submit_basic_information"
    ),
    path(
        route="submit_project_course/",
        view=views.CreateProjectView.as_view(),
        name="submit_project_course"
    ),
]