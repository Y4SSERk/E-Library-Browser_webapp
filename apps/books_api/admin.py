from django.contrib import admin
from .models import Author, Book, Subject

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Subject)