from django.core.management.base import BaseCommand
from apps.books_api.models import Subject

class Command(BaseCommand):
    help = 'Loads a comprehensive list of book subjects and categories'

    def handle(self, *args, **options):
        subjects_data = {
            # Genres (Fiction)
            'genre': [
                'Fantasy', 'Science Fiction', 'Mystery', 'Thriller', 'Romance',
                'Horror', 'Historical Fiction', 'Literary Fiction', 'Adventure',
                'Young Adult', 'Children\'s', 'Dystopian', 'Urban Fantasy',
                'Magical Realism', 'Contemporary', 'Paranormal', 'Western',
                'Cyberpunk', 'Steampunk', 'Noir', 'Graphic Novel', 'Fairy Tale',
                'Mythology', 'Satire', 'Absurdist'
            ],
            
            # Genres (Non-Fiction)
            'nonfiction': [
                'Biography', 'Memoir', 'Autobiography', 'History', 'Science',
                'Psychology', 'Philosophy', 'Politics', 'Economics', 'Business',
                'Technology', 'Computer Science', 'Mathematics', 'Physics',
                'Biology', 'Chemistry', 'Medicine', 'Health', 'Nutrition',
                'Self Help', 'Travel', 'Guidebook', 'True Crime', 'Journalism',
                'Essay', 'Criticism', 'Art', 'Music', 'Film', 'Photography',
                'Architecture', 'Design', 'Fashion', 'Sports', 'Cooking',
                'Gardening', 'Crafts', 'Education', 'Reference', 'Dictionary'
            ],
            
            # Themes
            'theme': [
                'Love', 'War', 'Coming of Age', 'Family', 'Friendship',
                'Betrayal', 'Revenge', 'Justice', 'Power', 'Corruption',
                'Identity', 'Race', 'Gender', 'Sexuality', 'Class', 'Poverty',
                'Wealth', 'Technology', 'Nature', 'Environment', 'Climate Change',
                'Artificial Intelligence', 'Space Exploration', 'Time Travel',
                'Alternative History', 'Utopia', 'Dystopia', 'Religion',
                'Spirituality', 'Atheism', 'Existentialism', 'Nihilism',
                'Human Condition', 'Isolation', 'Mental Health', 'Addiction',
                'Trauma', 'Recovery', 'Immigration', 'Colonialism', 'Revolution'
            ],
            
            # Settings/Places
            'place': [
                'New York', 'London', 'Paris', 'Tokyo', 'Rome', 'Berlin',
                'Moscow', 'Beijing', 'Shanghai', 'Hong Kong', 'Sydney',
                'Melbourne', 'Toronto', 'Vancouver', 'Los Angeles', 'Chicago',
                'San Francisco', 'Boston', 'Washington D.C.', 'New Orleans',
                'Mumbai', 'Delhi', 'Bangalore', 'Dubai', 'Singapore', 'Seoul',
                'Bangkok', 'Amsterdam', 'Barcelona', 'Madrid', 'Venice',
                'Prague', 'Vienna', 'Cairo', 'Nairobi', 'Cape Town',
                'Rio de Janeiro', 'Buenos Aires', 'Mexico City',
                # Fictional places
                'Middle Earth', 'Hogwarts', 'Narnia', 'Westeros', 'Gotham City',
                # Continents/regions
                'Africa', 'Asia', 'Europe', 'North America', 'South America',
                'Oceania', 'Middle East', 'Scandinavia', 'Balkans', 'Caribbean'
            ],
            
            # Time Periods
            'time_period': [
                'Ancient', 'Medieval', 'Renaissance', 'Victorian',
                'Edwardian', 'World War I', 'Interwar Period', 'World War II',
                'Cold War', 'Post-War', '1960s', '1970s', '1980s', '1990s',
                '2000s', 'Contemporary', 'Future', 'Prehistoric',
                'Industrial Revolution', 'Enlightenment', 'Prohibition Era',
                'Civil Rights Movement', 'Space Age', 'Digital Age',
                # Specific years/decades
                '1920s', 'Roaring Twenties', 'Great Depression', '1950s'
            ]
        }

        # Load subjects
        for subject_type, subjects in subjects_data.items():
            for subject_name in subjects:
                Subject.objects.update_or_create(
                    name=subject_name,
                    defaults={'subject_type': subject_type}
                )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded {Subject.objects.count()} subjects'
        ))