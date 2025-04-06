from django.core.management.base import BaseCommand
from apps.books_api.models import Country, Language
import pycountry

class Command(BaseCommand):
    help = 'Loads ISO country and language data into database'

    def handle(self, *args, **options):
        self.load_countries()
        self.load_languages()
        self.stdout.write(self.style.SUCCESS('Successfully loaded geographic data'))

    def load_countries(self):
        for country in pycountry.countries:
            Country.objects.update_or_create(
                code=country.alpha_2,
                defaults={
                    'name': country.name,
                    'official_name': getattr(country, 'official_name', None),
                    'three_letter_code': country.alpha_3,
                    'numeric_code': country.numeric,
                    'alternate_names': getattr(country, 'alt_names', []),
                }
            )

    def load_languages(self):
        for lang in pycountry.languages:
            if not hasattr(lang, 'alpha_2'):
                continue  # Skip languages without 2-letter codes

            Language.objects.update_or_create(
                code=lang.alpha_2,
                defaults={
                    'name': lang.name,
                    'three_letter_code': lang.alpha_3,
                    'bibliographic_code': getattr(lang, 'bibliographic', ''),
                    'alternate_names': getattr(lang, 'alt_names', []),
                }
            )