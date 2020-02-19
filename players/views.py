"""Player views"""

# Django Utilities
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import check_password
from django.views.generic import DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Django Models
from django.contrib.auth.models import User

# My models
from players.models import Player

# Exceptions
from django.db.utils import IntegrityError

# Forms
from players.forms import PlayerForm

# Utilities
from datetime import datetime, date
from email.mime.image import MIMEImage
import os


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'players/player.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    # Query set, a partir de qué lugar traerá los datos
    queryset = User.objects.all()
    context_object_name = 'user'


class AdminPanelView(LoginRequiredMixin, DetailView):
    template_name = 'players/admin_panel.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'


class LoginView(auth_views.LoginView):
    template_name = 'players/index.html'

    def form_invalid(self, login_form):
        return self.render_to_response(
            self.get_context_data(
                login_form=login_form
            )
        )


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'players/index.html'


class SignupView(FormView):
    model = Player
    template_name = 'players/index.html'
    form_class = PlayerForm
    fields = [
        'frist_name',
        'last_name', 
        'username', 
        'email', 
        'password', 
        'confirm_password', 
        'day',
        'month',
        'year'
    ]
    username = None

    def post(self, request, *args, **kwargs):
        signup_form = PlayerForm(self.request.POST)
        if signup_form.is_valid():
            return self.form_valid(signup_form)
        else:
            return self.form_invalid(signup_form)

    def form_valid(self, signup_form):
        signup_form.save()
        self.username = signup_form.cleaned_data['username']
        return super().form_valid(signup_form)

    def form_invalid(self, signup_form):
        return self.render_to_response(
            self.get_context_data(
                signup_form=signup_form
            )
        )

    def get_success_url(self):
        return reverse_lazy('players:login')


def index(request):
    days = [i for i in range(1, 31)]
    years = [2005 - i for i in range(1, 46)]
    months = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }
    try:
        user = User.objects.get(email=request.user.email)
    except AttributeError:
        user = None
    return render(request, 'players/index.html', { "days": days, "months": months, "years": years, 'user': user })