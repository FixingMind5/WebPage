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
        view=views.LoginView.as_view(), 
        name='login'
    ),
    path(
        route='signup/', 
        view=views.SignupView.as_view(), 
        name='signup'
    ),
    path(
        route='logout/', 
        view=views.LogoutView.as_view(), 
        name='logout'
    ),
    path(
        route='admin_panel/<str:username>',
        view=views.AdminPanelView.as_view(),
        name="admin_panel"
    ),
    path(
        route='me/profile/',
        view=views.UpdateUserView.as_view(),
        name='edit_player'
    ),
    path(
        route='<str:username>', 
        view=views.UserDetailView.as_view(), 
        name='player'
    ),
]