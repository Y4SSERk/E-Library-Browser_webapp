from django.db import models

class Author(models.Model):
    olid = models.CharField(max_length=20, unique=True)  # e.g., "OL34184A"
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.CharField(max_length=50, blank=True, null=True)
    death_date = models.CharField(max_length=50, blank=True, null=True)
    photos = models.JSONField(default=list, blank=True)  # List of photo IDs
    links = models.JSONField(default=list, blank=True)   # List of {"url": "...", "title": "..."}
    wikipedia = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)  # e.g., "Fantasy", "Science Fiction"
    
    def __str__(self):
        return self.name
    
class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)  # ISO 3166-1 alpha-2 (e.g., "US")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    # Identifiers
    olid = models.CharField(max_length=20, unique=True)  # e.g., "OL45804W"
    isbn_10 = models.CharField(max_length=10, blank=True, null=True)
    isbn_13 = models.CharField(max_length=13, blank=True, null=True)
    lccn = models.CharField(max_length=50, blank=True, null=True)  # Library of Congress Control Number
    oclc = models.CharField(max_length=50, blank=True, null=True)  # OCLC number

    # Core Metadata
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publish_date = models.CharField(max_length=50, blank=True, null=True)
    publishers = models.JSONField(default=list, blank=True)  # List of publishers
    languages = models.JSONField(default=list, blank=True)   # List of language codes (e.g., "eng")
    
    # Physical Details
    number_of_pages = models.IntegerField(blank=True, null=True)
    physical_format = models.CharField(max_length=100, blank=True, null=True)  # "Hardcover", "PDF", etc.
    weight = models.CharField(max_length=50, blank=True, null=True)  # e.g., "14.2 ounces"
    dimensions = models.CharField(max_length=100, blank=True, null=True)  # e.g., "9 x 6 x 1 inches"

    # Content
    description = models.TextField(blank=True, null=True)  # Plain text or HTML
    first_sentence = models.TextField(blank=True, null=True)
    table_of_contents = models.JSONField(default=list, blank=True)  # List of chapters
    
    # Categorization
    subjects = models.ManyToManyField(Subject, related_name='books')  # Genres/topics
    subject_places = models.JSONField(default=list, blank=True)  # e.g., ["Middle Earth"]
    subject_people = models.JSONField(default=list, blank=True)  # e.g., ["Bilbo Baggins"]
    subject_times = models.JSONField(default=list, blank=True)  # e.g., ["Third Age"]

    # Cover & Media
    cover_url = models.URLField(blank=True, null=True)  # Large cover image
    cover_thumbnail = models.URLField(blank=True, null=True)  # Small thumbnail
    preview_url = models.URLField(blank=True, null=True)  # Link to read online

    # Work Data (for editions)
    work_olid = models.CharField(max_length=20, blank=True, null=True)  # Parent work ID
    edition_count = models.IntegerField(blank=True, null=True)

    # Countries mentioned in content
    publish_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    subject_countries = models.ManyToManyField(Country, related_name='books_subject')  

    def __str__(self):
        return self.title