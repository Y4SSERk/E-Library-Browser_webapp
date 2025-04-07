from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Profile, Shelf
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm, ShelfCreateForm

# Shelf Views

@login_required
def saved(request):
    shelf = get_object_or_404(Shelf, profile=request.user.profile, shelf_type='SAVED')
    return render(request, 'accounts/shelf.html', {'shelf': shelf})

@login_required
def borrowed(request):
    shelf = get_object_or_404(Shelf, profile=request.user.profile, shelf_type='BORROWED')
    return render(request, 'accounts/shelf.html', {'shelf': shelf})

@login_required
def purchased(request):
    shelf = get_object_or_404(Shelf, profile=request.user.profile, shelf_type='PURCHASED')
    return render(request, 'accounts/shelf.html', {'shelf': shelf})

# Authentication Views
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically creates profile via signal
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Profile Views
@login_required
def profile(request):
    try:
        profile = request.user.profile
        shelves = profile.shelves.all()
        return render(request, 'profile/profile.html', {
            'profile': profile,
            'shelves': shelves
        })
    except Profile.DoesNotExist:
        # Handle case where profile doesn't exist (shouldn't happen with signal)
        Profile.objects.create(user=request.user)
        return redirect('profile')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'profile/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# Shelf Management
@login_required
def create_shelf(request):
    if request.method == 'POST':
        form = ShelfCreateForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ShelfCreateForm(user=request.user)
    
    return render(request, 'profile/create_shelf.html', {'form': form})