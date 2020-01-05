from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from players import views as players_app_views
from courses import views as courses_app_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Players
    path('player/', players_app_views.return_user, name='player'),
    path('login/', players_app_views.return_login, name='login'),
    path('signup/', players_app_views.signup, name='signup'),
    path('logout/', players_app_views.log_out, name='logout'),
    path('', players_app_views.index, name="index"),
    path('staff/', players_app_views.staff_panel, name="staff"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', players_app_views.activate, name='activate'),
    path('forgotten/', players_app_views.forgotten_password_page, name="forgotten"),
    path('email_retrieve_password/', players_app_views.send_email_retrieve_password, name="email_retrieve_password"),
    url(r'^retrieve_password_template/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', players_app_views.retrieve_password_template, name="retrieve_password_template"),
    url(r'retrieve_password/(?P<uidb64>[0-9A-Za-z_\-]+)/$', players_app_views.retrieve_password, name='retrieve_password'),

    # Courses
    path('add_course/', courses_app_views.add_course, name="add_course"),
    path('upload_course', courses_app_views.upload_course, name="upload_course")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
