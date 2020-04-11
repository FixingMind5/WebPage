from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from skyhackDjangoWeb.players import views as players_app_views
from skyhackDjangoWeb.courses import views as courses_app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Players
    path('', include(('skyhackDjangoWeb.players.urls', 'players'), namespace='players')),
    # Courses
    path('courses/', include(('skyhackDjangoWeb.courses.urls', 'courses'), namespace='courses')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
