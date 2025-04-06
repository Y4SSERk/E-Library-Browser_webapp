from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('shelf/saved', views.saved, name='saved'),
    path('shelf/borrowed', views.borrowed, name='borrowed'),
    path('shelf/purchased', views.purchased, name='purchased'),
]