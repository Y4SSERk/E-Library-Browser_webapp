from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, Shelf

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []  # Add profile-specific fields here if you expand the model

class ShelfCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Only allow custom shelves to be created through the form
        self.fields['shelf_type'].choices = [('CUSTOM', 'Custom Shelf')]
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Shelf
        fields = ['name', 'shelf_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter shelf name',
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Shelf.objects.filter(profile=self.user.profile, name=name).exists():
            raise ValidationError("You already have a shelf with this name.")
        return name

    def save(self, commit=True):
        shelf = super().save(commit=False)
        shelf.profile = self.user.profile
        if commit:
            shelf.save()
        return shelf

class ShelfUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable editing for default shelves
        if self.instance.shelf_type != 'CUSTOM':
            self.fields['name'].disabled = True
            self.fields['shelf_type'].disabled = True
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Shelf
        fields = ['name', 'shelf_type']