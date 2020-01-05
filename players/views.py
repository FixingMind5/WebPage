# Django Utilities
from django.conf import settings
from django.shortcuts import render, redirect
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

# Django Models
from django.contrib.auth.models import User

# My models
from players.models import Player

# Exceptions
from django.db.utils import IntegrityError


# Utilities
# from skyhackDjangoWeb.backends import email_authentication
from datetime import datetime, date
from email.mime.image import MIMEImage
import os


@login_required
def return_user(request):
    user_email = request.user.email
    user = User.objects.get(email=user_email)
    player = user.player
    user_data = {
        'username': request.user.username,
        'player_image': player.image,
        'points': player.points,
        'cluster': player.cluster,
        'grade': player.grade,
        'staff': request.user.is_staff,
        'description': player.description,
        'facebook': player.facebook,
        'twitter': player.twitter,
        'instagram': player.instagram,
        'youtube': player.youtube,
        'website': player.website
    }
    print(player.image.url == True)
    # request.user.is_staff
    return render(request, 'players/player.html', user_data)


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
            return redirect('player')
        else:
            return render(request, 'players/index.html', {'error': True})
    return render(request, 'players/index.html')


@login_required
def log_out(request):
    logout(request)
    return redirect('index')


def signup(request):
    if request.method == 'POST':
        """User registration"""
        # Obtaining basic user information
        name = request.POST['name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email'] # email for validation
        password = request.POST['password']
        passwordConfirmation = request.POST['confirm_password']

        # Obtaining user age
        current_year = date.year.__get__(date.today())
        birth_year = request.POST['year']
        age = int(current_year) - int(birth_year)
        
        birth_date_str = request.POST['day'] + "/" + request.POST['month'] + "/" + request.POST['year']
        birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y")

        #Checking if password matches
        if password != passwordConfirmation:
            # If no then return an error message
            return render(request, 'players/index.html', {'error': 'Passwords does not match'})
        try:
            # Creating a user and adding his password
            user = User.objects.create(username=username)
            user.set_password(raw_password=password)
        except IntegrityError:
            # Checking if another user with the same username is already registered
            return render(request, 'players/index.html', {'error': 'Username is already taken :('})
        # Adding last information 
        user.first_name = name
        user.last_name = lastname
        user.email = email
        user.is_active = False
        user.save()

        try:
            player = Player.objects.create(user=user, birth_date=birth_date, age=age, email=email)
            player.save()
        except IntegrityError:
            return render(request, 'players/index.html', {'error': 'User or email already taken'})

        # Creating email confirmation
        email_confirmation_message = False
        current_site = get_current_site(request)
        mail_subject = 'Activa tu cuenta 💪'
        message = render_to_string('players/account_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user_email = user.email
        email = EmailMultiAlternatives(
            mail_subject, message, to=[user_email]
        )
        email.attach_alternative(message, "text/html")

        email.send()
        email_confirmation_message = True

        return render(request, 'players/index.html', { "message": email_confirmation_message })
    return render(request, 'players/register.html')


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