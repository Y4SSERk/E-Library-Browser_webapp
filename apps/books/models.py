from django.db import models

'''
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    cover_image = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
'''