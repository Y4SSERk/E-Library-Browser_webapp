from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def map(request):
    return render(request, 'books/map.html')

def browse(request):
    return render(request, 'books/browse.html')

# more views can be added here

def books(request):
    return render(request, 'books/list.html')

def book(request):
    return render(request, 'books/details.html')
