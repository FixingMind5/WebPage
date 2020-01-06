# Django utilities
from django.urls import path

from courses import views

urlpatterns = [
    path(
        route='add_course/', 
        view=views.add_course, 
        name="add_course"
    ),
    # path(
    #     route='upload_course', 
    #     view=views.CreateCourseView.as_view(), 
    #     name="upload_course"
    # ),
]