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
from django.db.models import Q, Prefetch
from django.core.paginator import Paginator
from .models import Book, Author, Country, Subject, Language
import logging

logger = logging.getLogger(__name__)

def book_mega_filter(request):
    """
    Enhanced book filter with comprehensive subject handling
    """
    try:
        # ===== 1. PARSE AND VALIDATE FILTERS =====
        filters = {
            # Basic filters
            'title': request.GET.get('title', '').strip(),
            'author': request.GET.get('author', '').strip(),
            'publish_year': request.GET.get('publish_year', '').strip(),
            'language': request.GET.get('language', '').strip(),
            'min_pages': request.GET.get('min_pages'),
            'max_pages': request.GET.get('max_pages'),
            
            # Subject filters
            'subject': request.GET.get('subject', '').strip(),
            'genre': request.GET.get('genre', '').strip(),
            'theme': request.GET.get('theme', '').strip(),
            'place': request.GET.get('place', '').strip(),
            'time_period': request.GET.get('time_period', '').strip(),
            'demographic': request.GET.get('demographic', '').strip(),
            
            # Technical filters
            'has_cover': request.GET.get('has_cover'),
            'availability': request.GET.get('availability', '').strip(),
            'format': request.GET.get('format', '').strip(),
            
            # Pagination
            'page': request.GET.get('page', 1),
            'page_size': request.GET.get('page_size', 20),
        }

        # ===== 2. BUILD QUERY =====
        query = Q()
        
        # ----- Basic Filters -----
        if filters['title']:
            query &= Q(title__icontains=filters['title'])
        if filters['author']:
            query &= Q(authors__name__icontains=filters['author'])
        if filters['publish_year'] and filters['publish_year'].isdigit():
            query &= Q(publish_date__startswith=filters['publish_year'])
        if filters['min_pages'] and filters['min_pages'].isdigit():
            query &= Q(number_of_pages__gte=int(filters['min_pages']))
        if filters['max_pages'] and filters['max_pages'].isdigit():
            query &= Q(number_of_pages__lte=int(filters['max_pages']))

        # ----- Language Filter -----
        if filters['language']:
            try:
                lang = Language.objects.filter(
                    Q(code__iexact=filters['language']) |
                    Q(three_letter_code__iexact=filters['language']) |
                    Q(name__icontains=filters['language']) |
                    Q(alternate_names__contains=[filters['language']])
                ).first()
                if lang:
                    query &= Q(languages=lang)
            except Exception as e:
                logger.warning(f"Language filter error: {e}")

        # ----- Subject Filters -----
        if filters['subject']:
            query &= Q(subjects__name__icontains=filters['subject'])

        if filters['genre']:
            query &= Q(subjects__name__icontains=filters['genre'], 
                      subjects__subject_type='genre')

        if filters['theme']:
            query &= Q(subjects__name__icontains=filters['theme'],
                      subjects__subject_type='theme')

        if filters['place']:
            query &= (
                Q(subjects__name__icontains=filters['place'], 
                 subjects__subject_type='place') |
                Q(subject_places__contains=[filters['place']])
            )

        if filters['time_period']:
            query &= (
                Q(subjects__name__icontains=filters['time_period'],
                 subjects__subject_type='time_period') |
                Q(subject_times__contains=[filters['time_period']])
            )

        if filters['demographic']:
            query &= Q(subjects__name__icontains=filters['demographic'],
                      subjects__subject_type='demographic')

        # ----- Technical Filters -----
        if filters['has_cover'] == 'true':
            query &= Q(cover_url__isnull=False)
        elif filters['has_cover'] == 'false':
            query &= Q(cover_url__isnull=True)
        if filters['availability']:
            query &= Q(availability__iexact=filters['availability'])
        if filters['format']:
            query &= Q(physical_format__iexact=filters['format'])

        # ===== 3. EXECUTE QUERY =====
        books = Book.objects.filter(query).distinct() \
            .select_related('publish_country') \
            .prefetch_related(
                Prefetch('authors', queryset=Author.objects.select_related('birth_country')),
                Prefetch('subjects', queryset=Subject.objects.all()),
                'languages'
            ) \
            .order_by('title')

        # ===== 4. PAGINATION =====
        paginator = Paginator(books, int(filters['page_size']))
        page_obj = paginator.get_page(filters['page'])

        # ===== 5. BUILD RESPONSE =====
        results = []
        for book in page_obj:
            book_data = {
                'id': book.olid,
                'title': book.title,
                'authors': [
                    {
                        'name': author.name,
                        'country': author.birth_country.name if author.birth_country else None,
                        'country_code': author.birth_country.code if author.birth_country else None
                    } for author in book.authors.all()
                ],
                'publish_year': book.publish_date[:4] if book.publish_date else None,
                'publish_country': {
                    'name': book.publish_country.name if book.publish_country else None,
                    'code': book.publish_country.code if book.publish_country else None
                },
                'subjects': {
                    'all': list(book.subjects.values_list('name', flat=True)),
                    'by_type': {
                        'genres': list(book.subjects.filter(subject_type='genre')
                                      .values_list('name', flat=True)),
                        'themes': list(book.subjects.filter(subject_type='theme')
                                      .values_list('name', flat=True)),
                        'places': list(book.subjects.filter(subject_type='place')
                                      .values_list('name', flat=True)) + book.subject_places,
                        'time_periods': list(book.subjects.filter(subject_type='time_period')
                                           .values_list('name', flat=True)) + book.subject_times
                    }
                },
                'cover_url': book.cover_url,
                'pages': book.number_of_pages,
                'languages': [lang.code for lang in book.languages.all()],
                'format': book.physical_format,
                'availability': book.availability
            }
            results.append(book_data)

        return JsonResponse({
            'success': True,
            'count': paginator.count,
            'page': page_obj.number,
            'page_size': paginator.per_page,
            'total_pages': paginator.num_pages,
            'results': results
        })

    except Exception as e:
        logger.error(f"Filter error: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': "An error occurred while filtering books"
        }, status=400)