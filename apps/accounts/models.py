from django.db import models
from django.contrib.auth.models import User
# from apps.books.models import Book
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
class User: 
    username, 
    password, 
    email, 
    first_name,
    last_name
"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    def create_default_shelves(self):
        # Creates default shelves when a new profile is created.
        Shelf.objects.get_or_create(profile=self, shelf_type='SAVED', defaults={'name': 'Saved Books'})
        Shelf.objects.get_or_create(profile=self, shelf_type='BORROWED', defaults={'name': 'Borrowed Books'})
        Shelf.objects.get_or_create(profile=self, shelf_type='PURCHASED', defaults={'name': 'Purchased Books'})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.create_default_shelves()

class Shelf(models.Model):
    SHELF_TYPES = [
        ('SAVED', 'Saved Books'),
        ('BORROWED', 'Borrowed Books'),
        ('PURCHASED', 'Purchased Books'),
        ('CUSTOM', 'Custom Shelf'),  
    ]
        
    # Link the Shelf to a Profile (One Profile can have multiple Shelves)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='shelves')
    shelf_type = models.CharField(max_length=10, choices=SHELF_TYPES, default='CUSTOM')
    name = models.CharField(max_length=100)
    # books = models.ManyToManyField(Book, related_name='shelves', blank=True)

    def __str__(self):
        return f"{self.profile.user.username}'s {self.name}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'shelf_type'],
                name='unique_default_shelves',
                condition=models.Q(shelf_type__in=['SAVED', 'BORROWED', 'PURCHASED']),
            )
        ]