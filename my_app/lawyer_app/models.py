from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import RegexValidator,MaxLengthValidator
from django.utils import timezone
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    


class Lawyer(models.Model):
    lawyer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='lawyer_profile'
    )
    specialization = models.CharField(max_length=100, null=True, blank=True)  # Can be filled in later
    address = models.TextField(
        validators=[MaxLengthValidator(250)],
        null=True,
        blank=True
    )
    mobile_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r'^\+\d{1,3}\d{9,15}$', 
                message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed."
            )
        ],
        null=True,
        blank=True,  
        unique=True
    )
    registered_at = models.DateTimeField(default=timezone.now, editable=False)
    profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} (Lawyer ID: {self.lawyer_id})"

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='client_profile'
    )
    address = models.TextField(
        validators=[MaxLengthValidator(250)],
        null=True,  
        blank=True  
    )
    mobile_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r'^\+\d{1,3}\d{9,15}$',
                message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed."
            )
        ],
        null=True, 
        blank=True, 
        unique=True
    )
    registered_at = models.DateTimeField(default=timezone.now, editable=False)
    profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} (Client ID: {self.client_id})"

class Case(models.Model):
    case_id = models.AutoField(primary_key=True)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='cases')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cases')
    case_name = models.CharField(max_length=255)
    case_description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.case_name

class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    case = models.ForeignKey(Case, on_delete = models.CASCADE)

    DOCUMENT_TYPE_CHOICES = [
        ('brief', 'Brief'),
        ('contract', 'Contract'),
        ('memo', 'Memo'),
    ]
    document_type = models.CharField(max_length=100, choices=DOCUMENT_TYPE_CHOICES)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.document_id)


class LegalResearch(models.Model):
        research_id = models.AutoField(primary_key=True)
        research_topic = models.CharField(max_length = 200)
        researcher_name = models.CharField(max_length = 200)
        case = models.ForeignKey(Case, on_delete = models.CASCADE)

        def __str__ (self):
            return str(self.research_id)

