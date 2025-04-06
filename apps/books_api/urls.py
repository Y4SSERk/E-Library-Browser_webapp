from django.urls import path
from . import views
from .views import book_mega_filter

urlpatterns = [
    path('', views.home, name='home'),
    path('map', views.map, name='map'),
    path('browse', views.browse, name='browse'),
    path('filter/', book_mega_filter, name='book_mega_filter'),
]