from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


@login_required
def return_user(request):
    return render(request, 'players/player.html', {'players': 'players'})


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


def return_signin(request):
    return render(request, 'players/register.html')
