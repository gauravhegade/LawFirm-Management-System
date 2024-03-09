from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DocumentForm(forms.Form):
    document_id = forms.IntegerField(label='Document ID')
    document_type = forms.CharField(label='Document Type', max_length=100)
    case_id = forms.CharField(label='Case ID', max_length=100)
    update_date = forms.DateField(label='Update Date')