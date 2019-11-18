from django.contrib import admin
from django.urls import path

from players import views as players_app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('player/', players_app_views.returnUser)
]
