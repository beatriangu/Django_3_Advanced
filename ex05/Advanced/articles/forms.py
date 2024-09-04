from django import forms
from django.contrib.auth.forms import AuthenticationForm  # Import AuthenticationForm
from .models import Article, Favourite

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'author', 'synopsis', 'content', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'synopsis': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'published_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom form for user authentication with Bootstrap styling.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

class EmptyForm(forms.ModelForm):
    """
    A form class with no fields used for views that don't need user input.
    """
    class Meta:
        model = Favourite
        fields = []  # No fields are included in this form

