from django import forms
from .models import Note
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'body')

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
