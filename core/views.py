from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.core import signing
from .helpers import send_activation_token, activate_and_login_user
from .forms import RegisterForm
from .models import User

def home(request):
    if request.user.is_authenticated():
        return redirect('profile')
    
    return redirect('login')

def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated():
        return redirect('profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                name=data['name'],
                email=data['email'],
                password=data['password2'],
                accepted_terms=data['accepted_terms'],
                receives_newsletter=data['receives_newsletter']
            )

            send_activation_token(request, user)

            return redirect('register_complete')
    else:
        form = RegisterForm()

    return render(request, 'register.html', { 'form': form })

def register_complete(request):
    return render(request, 'register_complete.html')

def register_activate(request, activation_key=None):
    if request.user.is_authenticated():
        return redirect('profile')

    result = activate_and_login_user(request, activation_key)
    if result:
        return redirect('profile')

    return render(request, 'register_activate.html')

@login_required
def profile(request):
    return render(request, 'profile.html')