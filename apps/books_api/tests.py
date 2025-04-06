from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Country, Author, Subject, Book
import json

class ModelTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            code='US',
            name='United States',
            continent='North America'
        )
        self.author = Author.objects.create(
            name='Test Author',
            birth_country=self.country
        )
        self.genre = Subject.objects.create(
            name='Fantasy',
            subject_type='genre'
        )
        self.book = Book.objects.create(
            olid='OL123',
            title='Test Book',
            publish_country=self.country,
            number_of_pages=100
        )
        self.book.authors.add(self.author)
        self.book.subjects.add(self.genre)

    def test_country_creation(self):
        self.assertEqual(self.country.name, 'United States')
        self.assertEqual(str(self.country), 'United States (US)')

    def test_author_creation(self):
        self.assertEqual(self.author.name, 'Test Author')
        self.assertEqual(self.author.birth_country.code, 'US')

    def test_book_creation(self):
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.origin_countries[0].code, 'US')

    def test_book_author_relationship(self):
        self.assertEqual(self.book.authors.first().name, 'Test Author')

    def test_book_subject_relationship(self):
        self.assertEqual(self.book.subjects.first().name, 'Fantasy')


class BookFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data
        cls.usa = Country.objects.create(
            code='US', 
            name='United States',
            continent='North America'
        )
        cls.france = Country.objects.create(
            code='FR', 
            name='France', 
            continent='Europe'
        )
        
        cls.author1 = Author.objects.create(
            name='American Writer',
            birth_country=cls.usa
        )
        cls.author2 = Author.objects.create(
            name='French Writer',
            birth_country=cls.france
        )
        
        cls.genre = Subject.objects.create(
            name='Science Fiction',
            subject_type='genre'
        )
        cls.place = Subject.objects.create(
            name='Paris',
            subject_type='place'
        )
        
        # Book 1 - US author, Fantasy, 200 pages
        cls.book1 = Book.objects.create(
            olid='OL1',
            title='American Sci-Fi',
            publish_country=cls.usa,
            languages=['en'],
            number_of_pages=200,
            physical_format='Hardcover',
            availability='free',
            cover_url='http://example.com/cover1.jpg'
        )
        cls.book1.authors.add(cls.author1)
        cls.book1.subjects.add(cls.genre)
        
        # Book 2 - French author, 300 pages, no cover
        cls.book2 = Book.objects.create(
            olid='OL2',
            title='Paris Adventures',
            publish_country=cls.france,
            languages=['fr'],
            number_of_pages=300,
            physical_format='Ebook',
            availability='borrow'
        )
        cls.book2.authors.add(cls.author2)
        cls.book2.subjects.add(cls.place)
        cls.book2.subject_places = ['Paris']

    def test_country_filter(self):
        response = self.client.get(
            reverse('book_filter'),
            {'country_code': 'US'}
        )
        data = json.loads(response.content)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['title'], 'American Sci-Fi')

    def test_author_origin_filter(self):
        response = self.client.get(
            reverse('book_filter'),
            {'author_origin': 'France'}
        )
        data = json.loads(response.content)
        self.assertEqual(data['results'][0]['authors'][0]['name'], 'French Writer')

    def test_combined_filters(self):
        response = self.client.get(
            reverse('book_filter'),
            {
                'min_pages': 200,
                'max_pages': 250,
                'format': 'Hardcover'
            }
        )
        data = json.loads(response.content)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['title'], 'American Sci-Fi')

    def test_pagination(self):
        response = self.client.get(
            reverse('book_filter'),
            {
                'page_size': 1,
                'page': 2
            }
        )
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['total_pages'], 2)

    def test_empty_results(self):
        response = self.client.get(
            reverse('book_filter'),
            {
                'country_code': 'JP'  # No Japanese books in test data
            }
        )
        data = json.loads(response.content)
        self.assertEqual(data['count'], 0)

    def test_response_structure(self):
        response = self.client.get(reverse('book_filter'))
        data = json.loads(response.content)
        book = data['results'][0]
        
        # Test nested structure
        self.assertIn('title', book)
        self.assertIn('authors', book)
        self.assertIn('publish_country', book)
        self.assertIn('format', book)
        self.assertIn('cover_url', book)
        
        # Test author data
        self.assertIn('name', book['authors'][0])
        self.assertIn('country', book['authors'][0])