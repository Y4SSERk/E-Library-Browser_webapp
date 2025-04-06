from django.contrib import admin

# Register your models here.
from .models import Profile, Shelf

admin.site.register(Profile)
admin.site.register(Shelf)

