# Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Forms builded
from courses.forms import CourseForm

# Models
from courses.models import Course

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            form.save()
            return redirect('player')
    else:
        form = CourseForm()

    data = {
        'first_name': request.user.first_name,
        'username': request.user.username,
        'cluster': request.user.player.cluster,
        'form': form,
        # 'errors': form.errors,
    }

    return render(request, 'players/add_course.html', data)