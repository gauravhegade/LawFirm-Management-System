from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.shortcuts import render
from django.views import View
from .models import Lawyer, Client, Case, Document, LegalResearch, CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_active')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_active=False)  # Only show unapproved users

    def approve_user(self, request, queryset):
        for user in queryset:
            user.is_active = True  # Activate the user
            user.save()
            # Optionally, send an email to the user informing them of the approval.
        self.message_user(request, "Selected users have been approved.")
    approve_user.short_description = "Approve selected users"

    actions = [approve_user]

    
# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'is_active')

#     def changelist_view(self, request, extra_context=None):
#         extra_context = {
#             'unapproved_users_url': '/admin/lawyer_app/unapproved-users/',
#             'all_users_url': '/admin/lawyer_app/all-users/',
#         }
#         return super().changelist_view(request, extra_context=extra_context)

        
#     def get_urls(self):
#         return [
#             path('unapproved-users/', self.admin_site.admin_view(self.unapproved_users_view), name='unapproved_users'),
#             path('all-users/', self.admin_site.admin_view(self.all_users_view), name='all_users'),
#             *super().get_urls(),
#         ]
    

#     def unapproved_users_view(self, request):
#         print("Unapproved users view called")  # Debugging statement
#         unapproved_users = CustomUser.objects.filter(is_active=False)
#         return render(request, 'admin/unapproved_users.html', {'unapproved_users': unapproved_users})

#     def all_users_view(self, request):
#         print("All users view called")  # Debugging statement
#         all_users = CustomUser.objects.all()
#         return render(request, 'admin/all_users.html', {'all_users': all_users})




class LawyerAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'mobile_number')
    search_fields = ('user__username', 'specialization')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_number')
    search_fields = ('user__username',)

# Register the models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Lawyer, LawyerAdmin)
admin.site.register(Client, ClientAdmin)

admin.site.register(Case)
admin.site.register(Document)
admin.site.register(LegalResearch)

# Register your models here.
# Register your models here.
