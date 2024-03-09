from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    # Add any additional form fields or customization here if needed
    user_type = forms.CharField(label='User Type', max_length=10)