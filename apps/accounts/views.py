from django.shortcuts import render, redirect
from .models import Profile
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

# Create your views here.
"""
def login(request):
    return render(request, 'accounts/authentication/login.html')

def register(request):
    return render(request, 'accounts/authentication/register.html')

def profile(request):
    return render(request, 'accounts/profile.html')
"""
# shelf
def saved(request):
    return render(request, 'accounts/shelf.html')

def borrowed(request):
    return render(request, 'accounts/shelf.html')

def purchased(request):
    return render(request, 'accounts/shelf.html')

# signup
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/accounts/profile')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'profile/profile.html', {'profile': profile})

def edit_profile(request):
    return render(request, 'profile/edit_profile.html')