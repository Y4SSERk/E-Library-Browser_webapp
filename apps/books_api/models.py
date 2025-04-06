from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)  # ISO 2-letter code
    name = models.CharField(max_length=100)
    official_name = models.CharField(max_length=200, blank=True, null=True)
    three_letter_code = models.CharField(max_length=3, blank=True, null=True)
    numeric_code = models.CharField(max_length=3, blank=True, null=True)
    alternate_names = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Subject(models.Model):
    SUBJECT_TYPES = [
        ('genre', 'Genre (Fiction)'),
        ('nonfiction', 'Genre (Non-Fiction)'),
        ('theme', 'Theme'),
        ('place', 'Place/Setting'),
        ('time_period', 'Time Period'),
        ('character', 'Character Type'),
        ('demographic', 'Audience Demographic'),
    ]

    name = models.CharField(max_length=200, unique=True)
    subject_type = models.CharField(
        max_length=20,
        choices=SUBJECT_TYPES,
        blank=True,
        null=True
    )
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    alternate_names = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['subject_type']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_subject_type_display() or 'generic'})"

class Author(models.Model):
    """
    Enhanced author model with nationality tracking
    """
    # Open Library ID
    olid = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.CharField(max_length=50, blank=True, null=True)
    death_date = models.CharField(max_length=50, blank=True, null=True)
    # Author's country of birth/origin
    birth_country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authors',
        to_field='code'  # Explicitly specify to use the 'code' field
    )
    # Other national affiliations
    other_countries = models.ManyToManyField(
        Country,
        blank=True,
        related_name='associated_authors'
    )

    def __str__(self):
        return f"{self.name} ({self.birth_country.code if self.birth_country else 'Unknown'})"

class Language(models.Model):
    """International standard language codes"""
    code = models.CharField(max_length=2, primary_key=True)  # ISO 639-1 (2-letter)
    name = models.CharField(max_length=100)
    three_letter_code = models.CharField(max_length=3)  # ISO 639-2/T
    bibliographic_code = models.CharField(max_length=3, blank=True)  # ISO 639-2/B
    alternate_names = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class Book(models.Model):
    """
    Comprehensive book model with geographical tracking
    """
    # Identifiers
    olid = models.CharField(max_length=20, unique=True)  # Open Library ID
    isbn_10 = models.CharField(max_length=10, blank=True, null=True)
    isbn_13 = models.CharField(max_length=13, blank=True, null=True)
    lccn = models.CharField(max_length=50, blank=True, null=True)  # Library of Congress
    
    # Core Metadata
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publish_date = models.CharField(max_length=50, blank=True, null=True)
    publish_country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='published_books',
        to_field='code'  # Explicitly specify to use the 'code' field
    )
    languages = models.ManyToManyField(Language, blank=True)
    publishers = models.JSONField(default=list)  # List of publisher names
    
    # Content Classification
    subjects = models.ManyToManyField(Subject, related_name='books')
    subject_places = models.JSONField(default=list)  # Places in content
    subject_times = models.JSONField(default=list)  # Time periods
    literary_awards = models.JSONField(default=list)
    
    # Physical Details
    number_of_pages = models.IntegerField(blank=True, null=True)
    physical_format = models.CharField(max_length=50, blank=True, null=True)
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=50, blank=True, null=True)
    
    # Digital Assets
    cover_url = models.URLField(blank=True, null=True)
    preview_url = models.URLField(blank=True, null=True)
    
    # Availability
    AVAILABILITY_CHOICES = [
        ('free', 'Free Access'),
        ('borrow', 'Borrow Only'),
        ('paid', 'Purchase Required'),
    ]
    availability = models.CharField(
        max_length=10,
        choices=AVAILABILITY_CHOICES,
        blank=True,
        null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['publish_date']),
            models.Index(fields=['publish_country']),
        ]
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.publish_date[:4] if self.publish_date else 'Unknown'})"

    @property
    def origin_countries(self):
        """Returns all countries associated with this book's origin"""
        countries = set()
        if self.publish_country:
            countries.add(self.publish_country)
        for author in self.authors.all():
            if author.birth_country:
                countries.add(author.birth_country)
        return list(countries)