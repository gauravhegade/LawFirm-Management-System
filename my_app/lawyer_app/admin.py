from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin,GroupAdmin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.models import Group
from .models import Lawyer, Client, Case, Document, LegalResearch, CustomUser
from django.contrib.admin import AdminSite
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_active')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #return qs.filter(is_active=False)  # Only show unapproved users
        return qs

    def approve_user(self, request, queryset):
        for user in queryset:
            user.is_active = True  # Activate the user
            user.save()

            #self.send_approval_email(user)

        self.message_user(request, "Selected users have been approved.")
    approve_user.short_description = "Approve selected users"

    def deactivate_user(self, request, queryset):
        for user in queryset:
            user.is_active = False   
            user.save()

            #self.send_deactivation_email(user)

        self.message_user(request, "Selected users have been deactivated and notified by email.")
    deactivate_user.short_description = "Deactivate selected users"

    actions = [approve_user,deactivate_user]

    def send_approval_email(self, user):
        subject = 'Your account has been approved'

        html_message = render_to_string('emails/approved_user.html', {
            'user': user,
            'login_url': f"{settings.SITE_URL}/login/" 
        })
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message, 
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
            html_message=html_message  # Include the HTML version
        )

    def send_deactivation_email(self, user):
        subject = 'Your Account Has Been Deactivated'

        html_message = render_to_string('emails/deactivated_user.html', {
            'user': user,
            'support_url': 'https://www.google.com' 
        })
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message, 
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
            html_message=html_message
        )

    

class CustomUserSite(AdminSite):
    # list_display = ('username', 'email', 'is_active')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('unapproved-users/', self.admin_view(self.unapproved_users_view), name='unapproved_users'),
            path('all-users/', self.admin_view(self.all_users_view), name='all_users'),
        ]
        return custom_urls + urls
    def unapproved_users_view(self, request):
        unapproved_users = CustomUser.objects.filter(is_active=False)
        return render(request, 'admin/unapproved_users.html', {'unapproved_users': unapproved_users})

    def all_users_view(self, request):
        all_users = CustomUser.objects.all()
        return render(request, 'admin/all_users.html', {'all_users': all_users})
    

class LawyerAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'mobile_number','is_active_status')
    search_fields = ('user__username', 'specialization')

    def is_active_status(self, obj):
        return obj.user.is_active
    is_active_status.short_description = 'Status'
    is_active_status.boolean = True
    
    def deactivate_lawyers(self, request, queryset):
        queryset.update(user__is_active=False)
        self.message_user(request, "Selected lawyers have been deactivated.")
    deactivate_lawyers.short_description = "Deactivate selected lawyers"

    
    def activate_lawyers(self, request, queryset):
        queryset.update(user__is_active=True)  
        self.message_user(request, "Selected lawyers have been activated.")
    activate_lawyers.short_description = "Activate selected lawyers"

    actions = [deactivate_lawyers, activate_lawyers]


class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_number','is_active_status')
    search_fields = ('user__username',)

    def is_active_status(self, obj):
        return obj.user.is_active
    is_active_status.short_description = 'Status'
    is_active_status.boolean = True


    def deactivate_clients(self, request, queryset):
        queryset.update(user__is_active=False) 
        self.message_user(request, "Selected clients have been deactivated.")
    deactivate_clients.short_description = "Deactivate selected clients"

    def activate_clients(self, request, queryset):
        queryset.update(user__is_active=True)
        self.message_user(request, "Selected clients have been activated.")
    activate_clients.short_description = "Activate selected clients"

    actions = [deactivate_clients, activate_clients]


site = CustomUserSite()
site.register(CustomUser, CustomUserAdmin)
site.register(Lawyer, LawyerAdmin)
site.register(Client, ClientAdmin)

site.register(Case)
site.register(Document)
site.register(LegalResearch)

site.register(Group, GroupAdmin)



