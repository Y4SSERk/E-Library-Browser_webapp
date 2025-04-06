from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'users/authentication/login.html')

def register(request):
    return render(request, 'users/authentication/register.html')

def profile(request):
    return render(request, 'users/profile.html')

# shelf
def saved(request):
    return render(request, 'users/shelf.html')

def borrowed(request):
    return render(request, 'users/shelf.html')

def purchased(request):
    return render(request, 'users/shelf.html')
