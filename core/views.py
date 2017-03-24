from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated():
        return redirect('profile')
    
    return redirect('auth_login')

@login_required
def profile(request):
    return render(request, 'profile.html')