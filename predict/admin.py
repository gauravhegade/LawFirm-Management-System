from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Lawyer)
admin.site.register(Client)
admin.site.register(Case)
admin.site.register(Documents)
admin.site.register(LegalResearch)

