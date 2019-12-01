from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from players.models import Player

# Exceptions
from django.db.utils import IntegrityError


@login_required
def return_user(request):
    data = {
        'username': request.user.username,
        'points': request.user.player.points,
        'cluster': request.user.player.cluster,
        'grade': request.user.player.grade,
        'staff': request.user.is_staff
    }
    # request.user.is_staff
    return render(request, 'players/player.html', data)


def return_login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['email'],
            password=request.POST['password']
        )
        # import pdb; pdb.set_trace()
        if user is not None:
            login(request, user)
            return redirect('player')
        else:
            return render(request, 'players/login.html', {'error': 'Invalid email or password'})
    return render(request, 'players/login.html')


@login_required
def log_out(request):
    logout(request)
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        userName = request.POST['userName']
        email = request.POST['email']
        emailConfirmation = request.POST['emailConfirmation']
        password = request.POST['password']
        passwordConfirmation = request.POST['passwordConfirmation']

        if email != emailConfirmation:
            return render(request, 'players/register.html', {'error': 'Emails does not match'})

        if password != passwordConfirmation:
            return render(request, 'players/register.html', {'error': 'Passwords does not match'})

        try:
            user = User.objects.create(username=userName)
            user.set_password(raw_password=password)
        except IntegrityError:
            return render(request, 'players/register.html', {'error': 'Username is already taken :('})
        user.first_name = request.POST['name']
        user.last_name = request.POST['lastName']
        user.email = email
        user.save()

        player = Player.objects.create(user=user, age=request.POST['age'])
        player.save()

        return redirect('login')
    return render(request, 'players/register.html')


def index(request):
    return render(request, 'players/index.html')

@login_required
def staff_panel(request):
    return render(request, 'players/staff_panel.html')