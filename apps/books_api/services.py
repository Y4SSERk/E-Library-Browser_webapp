import requests
from .models import Author, Book, Subject, Country
from django.core.exceptions import ObjectDoesNotExist

class OpenLibraryAPI:
    BASE_URL = "https://openlibrary.org"

    @classmethod
    def _fetch_data(cls, url):
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None

    @classmethod
    def fetch_book(cls, olid):
        """Fetch all data for a book/work."""
        return cls._fetch_data(f"{cls.BASE_URL}/works/{olid}.json")

    @classmethod
    def fetch_author(cls, olid):
        """Fetch all data for an author."""
        return cls._fetch_data(f"{cls.BASE_URL}/authors/{olid}.json")

    @classmethod
    def save_book_to_db(cls, olid):
        """Save a book and all related data to the database."""
        book_data = cls.fetch_book(olid)
        if not book_data:
            return None

        # Handle Authors
        authors = []
        for author_data in book_data.get("authors", []):
            author_olid = author_data["author"]["key"].split("/")[-1]
            author_db = Author.objects.filter(olid=author_olid).first()
            if not author_db:
                author_api_data = cls.fetch_author(author_olid)
                author_db = Author.objects.create(
                    olid=author_olid,
                    name=author_api_data.get("name", "Unknown"),
                    bio=author_api_data.get("bio", {}).get("value") if isinstance(author_api_data.get("bio"), dict) else author_api_data.get("bio"),
                    birth_date=author_api_data.get("birth_date"),
                    death_date=author_api_data.get("death_date"),
                    photos=author_api_data.get("photos", []),
                    links=author_api_data.get("links", []),
                    wikipedia=author_api_data.get("wikipedia", {}).get("url") if isinstance(author_api_data.get("wikipedia"), dict) else None,
                )
            authors.append(author_db)

        # Handle Subjects (Genres/Topics)
        subjects = []
        for subject_name in book_data.get("subjects", []):
            subject_db, _ = Subject.objects.get_or_create(name=subject_name)
            subjects.append(subject_db)

        # Create/Update Book
        book_db, created = Book.objects.update_or_create(
            olid=olid,
            defaults={
                # Identifiers
                "isbn_10": book_data.get("isbn_10", [""])[0] if book_data.get("isbn_10") else None,
                "isbn_13": book_data.get("isbn_13", [""])[0] if book_data.get("isbn_13") else None,
                "lccn": book_data.get("lccn", [""])[0] if book_data.get("lccn") else None,
                "oclc": book_data.get("oclc", [""])[0] if book_data.get("oclc") else None,
                
                # Core Metadata
                "title": book_data.get("title"),
                "subtitle": book_data.get("subtitle"),
                "publish_date": book_data.get("first_publish_date"),
                "publishers": book_data.get("publishers", []),
                "languages": [lang["key"] for lang in book_data.get("languages", [])],
                
                # Physical Details
                "number_of_pages": book_data.get("number_of_pages"),
                "physical_format": book_data.get("physical_format"),
                "weight": book_data.get("weight"),
                "dimensions": book_data.get("dimensions"),
                
                # Content
                "description": book_data.get("description", {}).get("value") if isinstance(book_data.get("description"), dict) else book_data.get("description"),
                "first_sentence": book_data.get("first_sentence", {}).get("value") if isinstance(book_data.get("first_sentence"), dict) else book_data.get("first_sentence"),
                "table_of_contents": [entry.get("title") for entry in book_data.get("table_of_contents", [])],
                
                # Categorization
                "subject_places": book_data.get("subject_places", []),
                "subject_people": book_data.get("subject_people", []),
                "subject_times": book_data.get("subject_times", []),
                
                # Cover & Media
                "cover_url": f"https://covers.openlibrary.org/b/olid/{olid}-L.jpg",
                "cover_thumbnail": f"https://covers.openlibrary.org/b/olid/{olid}-S.jpg",
                "preview_url": book_data.get("preview_url"),
                
                # Work Data
                "work_olid": book_data.get("work_olid"),
                "edition_count": book_data.get("edition_count"),
            }
        )
        
        # Set ManyToMany relationships
        book_db.authors.set(authors)
        book_db.subjects.set(subjects)

        # Handle Countries
        publish_country = None
        if book_data.get("publish_country"):
            try:
                publish_country = Country.objects.get(code=book_data["publish_country"])
            except ObjectDoesNotExist:
                # Auto-create country if not found (or skip)
                pass

        subject_countries = []
        for place in book_data.get("subject_places", []):
            # Extract country codes from place names (e.g., "United States" → "US")
            # You may need a lookup table or API like pycountry for this
            pass

        # Update book creation
        book_db, created = Book.objects.update_or_create(
            olid=olid,
            defaults={
                # ... (existing fields)
                "publish_country": publish_country,
            }
        )
        book_db.subject_countries.set(subject_countries)
        
        return book_db