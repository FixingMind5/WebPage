# Django utilities
from django.urls import path

from skyhackDjangoWeb.courses import views

urlpatterns = [
    path(
        route='add_course/', 
        view=views.CreateCourseView.as_view(), 
        name="add_course"
    ),
    path(
        route='add_lesson/',
        view=views.add_lesson,
        name="add_lesson"
    ),
    path(
        route='catalog',
        view=views.CourseCatalogView.as_view(),
        name='catalog',
    ),
    path(
        route='admin_course_detail/<str:course>',
        view=views.AdminCourseView.as_view(),
        name='admin_course_detail'
    ),
    path(
        route='<str:abreviation>',
        view=views.CourseDetailView.as_view(),
        name='course'
    ),
    path(
        route='<str:abreviation>/<int:pk>',
        view=views.LessonDetaiView.as_view(),
        name='lesson'
    ),
    path(
        route='<str:abreviation>/<int:lesson_pk>/add_comentary',
        view=views.AddComentaryView.as_view(),
        name='comentary'
    ),
    path(
        route='<str:abreviation>/<int:lesson_pk>/add_answer',
        view=views.AddAnswerView.as_view(),
        name='answer'
    ),
    path(
        route='<int:pk>/delete_comentary',
        view=views.AnswerDelete.as_view(),
        name='delete_comentary'
    )
]