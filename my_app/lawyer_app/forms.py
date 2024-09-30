from django import forms
#from django.contrib.auth.models import User
from .models import CustomUser, Lawyer,Client,Case
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError
import re


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)  
    last_name = forms.CharField(max_length=30, required=True)   
    
    ROLE_CHOICES = [
        ('lawyer', 'Lawyer'),
        ('client', 'Client'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'first_name', 'last_name']

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


class LawyerProfileForm(forms.ModelForm):
    class Meta:
        model = Lawyer
        fields = ['specialization', 'address', 'mobile_number']
    
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        phone_pattern = r'^\+\d{1,3}\d{9,15}$'
        if not re.match(phone_pattern, mobile_number):
            raise ValidationError("Invalid mobile number format. It should be in the format '+123456789'.")
        return mobile_number

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['address', 'mobile_number']

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        phone_pattern = r'^\+\d{1,3}\d{9,15}$'
        if not re.match(phone_pattern, mobile_number):
            raise ValidationError("Invalid mobile number format. It should be in the format '+123456789'.")
        return mobile_number
    
class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['client', 'case_name', 'case_description']