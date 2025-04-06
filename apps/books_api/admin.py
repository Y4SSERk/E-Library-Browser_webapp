from django.contrib import admin
from .models import Country, Author, Subject, Book, Language

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'three_letter_code')  # Removed 'continent'
    search_fields = ('name', 'code', 'three_letter_code')
    list_filter = ()  # Removed 'continent' from filters

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_country')
    search_fields = ('name',)
    list_filter = ('birth_country',)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject_type')
    search_fields = ('name',)
    list_filter = ('subject_type',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date_short', 'publish_country')
    search_fields = ('title', 'isbn_10', 'isbn_13')
    list_filter = ('publish_country', 'availability')
    filter_horizontal = ('authors', 'subjects')
    
    def publish_date_short(self, obj):
        return obj.publish_date[:4] if obj.publish_date else None
    publish_date_short.short_description = 'Year'

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'three_letter_code')
    search_fields = ('name', 'code', 'three_letter_code')
    list_filter = ('three_letter_code',)

admin.site.register(Country, CountryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Book, BookAdmin)