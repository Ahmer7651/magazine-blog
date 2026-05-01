from django import forms
from .models import Magazine, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class MagazineForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="---------",
        required=True
    )
    
    class Meta:
        model = Magazine
        fields = ['title', 'category','image', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your content here...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
        }

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

class SignupForm(UserCreationForm):
    email=forms.EmailField(required=True)
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=30)
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class SearchForm(forms.Form):
    query=forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'autocomplete':'off',
            'placeholder':'Search Magazines by title or author....',
            'class':'search-input'
        }
        )
    )