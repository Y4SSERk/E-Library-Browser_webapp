from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),

    path('shelves/saved/', views.saved, name='saved_shelf'),
    path('shelves/borrowed/', views.borrowed, name='borrowed_shelf'),
    path('shelves/purchased/', views.purchased, name='purchased_shelf'),
    path('shelves/create/', views.create_shelf, name='create_shelf'),
]