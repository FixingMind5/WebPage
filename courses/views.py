# Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Forms builded
from courses.forms import CourseForm

# Models
from courses.models import Course

@login_required
def add_course(request):
    email = request.user.email
    user = User.objects.get(email=email)
    player = user.player
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            form.save()
            return redirect('player')
    else:
        form = CourseForm()

    data = {
        'username': user.username,
        'form': form,
        # 'errors': form.errors,
    }

    return render(request, 'players/add_course.html', data)