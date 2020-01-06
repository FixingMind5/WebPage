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


@login_required
def return_user(request):
    return render(request, 'players/player.html')


def return_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = password=request.POST['password']
        user = authenticate (
            username=email,
            password=password
        )
        if user is not None:
            login(request, user)
            url = reverse('players:player', kwargs={'username': user.username})
            return redirect(url)
        else:
            return render(request, 'players/index.html', { 'error': True })
    return render(request, 'players/index.html')


@login_required
def log_out(request):
    logout(request)
    return redirect('players:index')


def send_email(request):
    # Creating email confirmation
    pass


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
    success_url = reverse_lazy('players:login')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        username = self.object.user.username
        return reverse_lazy('players:player', kwargs={ 'username': username })

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def signup(request):
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
    if request.method == 'POST':
        """User registration"""
        player_form = PlayerForm(request.POST)
        
        if player_form.is_valid():
            player_form.save()
            return render(request, 'players/index.html')

    else:
        player_form = PlayerForm()

    return render(
        request=request,
        template_name='players/index.html',
        context={
            'player_form': player_form,
            'days': [i for i in range(1, 31)],
            'years': [2005 - i for i in range(1, 46)],
            'months': months
        })


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid) # Obtaining user from primary key
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('player')
    else:
        return render(request, 'players/index.html', { 'invalid_message': True })


def forgotten_password_page(request):
    return render(request, "players/forgot_password.html")


def send_email_retrieve_password(request):
    if request.method == 'POST':
        email = request.POST["user_email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "players/index.html", { "is_retrieve_email_success": False })
        current_site = get_current_site(request)
        mail_subject = "Solicitud de cambio de contraseña"
        email_message = render_to_string("players/retrieve_password_email.html", {
            'user': user,
            'domain': current_site.domain,
            'user_id': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        email = EmailMultiAlternatives(
            mail_subject,
            email_message,
            to = [email]
        )
        email.attach_alternative(email_message, "text/html")
        email.send()

        return render(request, "players/index.html", { "is_retrieve_email_success": True } )
    return render(request, "players/index.html")
    

def retrieve_password_template(request, uidb64, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        return render(request, "players/retrieve_password_template.html", { 'user_id': uidb64 })
    return render(request, "players/index.html", { 'retrieve_password_error': True })


def retrieve_password(request, uidb64):
    if request.method == 'POST':
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        password = request.POST['new_password']
        password_confirmation = request.POST['confirm_new_password']
        success = password == password_confirmation
        if success:
            user.set_password(raw_password=password)
            user.save()
            return render(request, "players/index.html", { "is_password_changed": True })
        else:
            return render(request, "players/retrieve_password_template.html", { "is_password_changed": False, 'user_id': uidb64 })


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

@login_required
def staff_panel(request):
    return render(request, 'players/staff_panel.html')