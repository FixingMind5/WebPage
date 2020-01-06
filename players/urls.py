from django.urls import path
from django.views.generic import TemplateView

from players import views

urlpatterns = [
    path(
        route='',
        view=views.index,
        name="index"
        ),
    path(
        route='login/', 
        view=views.return_login, 
        name='login'
    ),
    path(
        route='signup/', 
        view=views.SignupView.as_view(), 
        name='signup'
    ),
    path(
        route='logout/', 
        view=views.log_out, 
        name='logout'
    ),
    path(
        route='<str:username>', 
        view=views.UserDetailView.as_view(), 
        name='player'
    ),
]