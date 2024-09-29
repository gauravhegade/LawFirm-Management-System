from django import forms
#from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='username',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'})
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'})
    )

class DocumentForm(forms.Form):
    document_id = forms.IntegerField(label='Document ID')
    document_type = forms.CharField(label='Document Type', max_length=100)
    case_id = forms.CharField(label='Case ID', max_length=100)
    update_date = forms.DateField(label='Update Date')