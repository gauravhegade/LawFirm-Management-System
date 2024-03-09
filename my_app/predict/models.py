from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



class Lawyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lawyer_profile',null=True, blank=True)
    lawyer_id = models.AutoField(primary_key=True)
    lawyer_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact_info = models.IntegerField()

    def __str__(self):
        return str(self.lawyer_id)    

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=255)
    address = models.TextField()
    contact_info = models.CharField(max_length=255)
    case = models.ForeignKey("Case", on_delete=models.CASCADE)

    def __str__(self):
        return self.client_name

class Case(models.Model):
    case_id = models.AutoField(primary_key=True)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    case_name = models.CharField(max_length=255)
    clients = models.ManyToManyField(Client, related_name='cases', through='ClientCaseRelationship')

    def __str__(self):
        return self.case_name

class Documents(models.Model):
    document_id = models.AutoField(primary_key=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    upload_date = models.CharField(max_length=100)

    def __str__(self):
        return str(self.document_id)

class LegalResearch(models.Model):
    research_id = models.AutoField(primary_key=True)
    research_topic = models.CharField(max_length=200)
    researcher_name = models.CharField(max_length=200)
    legal_case = models.ForeignKey(Case, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.research_id)

class ClientCaseRelationship(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
