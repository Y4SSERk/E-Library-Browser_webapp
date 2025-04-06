from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'accounts/authentication/login.html')

def register(request):
    return render(request, 'accounts/authentication/register.html')

def profile(request):
    return render(request, 'accounts/profile.html')

# shelf
def saved(request):
    return render(request, 'accounts/shelf.html')

def borrowed(request):
    return render(request, 'accounts/shelf.html')

def purchased(request):
    return render(request, 'accounts/shelf.html')
