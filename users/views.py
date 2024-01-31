from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UpdateUserForm
from .models import User
from events.models import Event


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('event_list')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('event_list')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('event_list')


def user_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    events = Event.objects.filter(creator=user)
    registered_events = Event.objects.filter(participants=user)
    return render(request, 'users/user_profile.html', {'user': user, 'events': events, 'registered_events': registered_events})


@login_required(login_url='login')
def update_user_view(request):
    user = request.user
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user', user_id=user.id)

    return render(request, 'users/update_user_profile.html', {'form': form})
