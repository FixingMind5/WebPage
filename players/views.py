# Django Utilities
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Django Models
from django.contrib.auth.models import User

# My models
from players.models import Player

# Exceptions
from django.db.utils import IntegrityError


# Utilities
from datetime import datetime, date



@login_required
def return_user(request):
    data = {
        'username': request.user.username,
        'points': request.user.player.points,
        'cluster': request.user.player.cluster,
        'grade': request.user.player.grade,
        'staff': request.user.is_staff,
    }
    # request.user.is_staff
    return render(request, 'players/player.html', data)


def return_login(request):
    if request.method == 'POST':
        user = authenticate (
            username=request.POST['email'],
            password=request.POST['password']
        )
        # import pdb; pdb.set_trace()
        if user is not None:
            login(request, user)
            return redirect('player')
        else:
            return render(request, 'players/index.html', {'error': 'Invalid email or password'})
    return render(request, 'players/index.html')


@login_required
def log_out(request):
    logout(request)
    return redirect('login')


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

        player = Player.objects.create(user=user, birth_date=birth_date, age=age)
        player.save()

        # Creating email confirmation
        current_site = get_current_site(request)
        mail_subject = 'Activa tu cuenta 💪'
        message = render_to_string('players/account_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            # 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[user_email]
        )
        email.send()
        print('Email sended')

        return redirect('login')
    return render(request, 'players/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid) # Obtaining user from primary key
        # import pdb; pdb.set_trace()
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        print(f"{user.is_active} activo")
        login(request, user)
        return HttpResponse('Gracias por confirmar tu registro. Ahora puedes ingresar')
    else:
        return HttpResponse('El link de activación es ¡inválido!')


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
    return render(request, 'players/index.html', { "days": days, "months": months, "years": years })

@login_required
def staff_panel(request):
    return render(request, 'players/staff_panel.html')