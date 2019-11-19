from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from players import views as players_app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('player/', players_app_views.return_user, name='player'),
    path('login/', players_app_views.return_login, name='login'),
    path('signup/', players_app_views.return_signup, name='signup'),
    path('logout/', players_app_views.log_out, name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
