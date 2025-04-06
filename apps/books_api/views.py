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

from django.http import JsonResponse
from django.db.models import Q
from .models import Book, Author, Subject, Country

def book_mega_filter(request):
    # Extract all possible filter parameters from GET request
    filters = {
        'title': request.GET.get('title'),
        'author': request.GET.get('author'),
        'subject': request.GET.get('subject'),
        'publish_year': request.GET.get('publish_year'),
        'language': request.GET.get('language'),
        'country': request.GET.get('country'),  # For SVG map
        'min_pages': request.GET.get('min_pages'),
        'max_pages': request.GET.get('max_pages'),
    }

    # Build the query dynamically
    query = Q()
    if filters['title']:
        query &= Q(title__icontains=filters['title'])
    if filters['author']:
        query &= Q(authors__name__icontains=filters['author'])
    if filters['subject']:
        query &= Q(subjects__name__icontains=filters['subject'])
    if filters['publish_year']:
        query &= Q(publish_date__startswith=filters['publish_year'])
    if filters['language']:
        query &= Q(languages__contains=[filters['language']])
    if filters['country']:
        query &= Q(publish_country__code=filters['country']) | Q(subject_countries__code=filters['country'])
    if filters['min_pages']:
        query &= Q(number_of_pages__gte=int(filters['min_pages']))
    if filters['max_pages']:
        query &= Q(number_of_pages__lte=int(filters['max_pages']))

    # Apply the query
    books = Book.objects.filter(query).distinct().select_related('publish_country').prefetch_related('authors', 'subjects')

    # Convert to JSON response
    results = []
    for book in books:
        results.append({
            'title': book.title,
            'authors': [author.name for author in book.authors.all()],
            'publish_year': book.publish_date,
            'country': book.publish_country.code if book.publish_country else None,
            'cover_url': book.cover_url,
            'id': book.olid,
        })

    return JsonResponse({'books': results})
