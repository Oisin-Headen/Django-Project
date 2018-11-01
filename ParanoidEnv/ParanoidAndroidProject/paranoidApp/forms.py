"""Forms for sign-ups"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SurveyUser

class SignUpForm(UserCreationForm):
    """Sign up Form"""
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    is_admin = forms.BooleanField(required=False, help_text="Are you an Admin?")

    class Meta:
        model = SurveyUser
        fields = ('username', 'first_name', 'last_name', 'is_admin', 'password1', 'password2', )
