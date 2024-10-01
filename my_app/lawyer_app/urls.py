from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


app_name = 'lawyer_app'

urlpatterns = [
    path('', views.info ,name='home'),
    path('login/', views.login_user, name='login'),
    path('upload-document', views.upload_document, name='upload_document'),
    path('lawyer/case-status/', views.case_status, name='case_status'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),

    path('client/<int:client_id>/', views.client_profile, name='client_profile'),
    path('lawyer/<int:lawyer_id>/', views.lawyer_profile, name='lawyer_profile'),

    path('client/approve-case/', views.approve_case, name='approve_case'),
    path('search-clients/', views.search_clients, name='search_clients'),
    path('search-casess/', views.search_cases, name='search_cases'),

    path('lawyer/dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('lawyer/create-case/', views.create_case, name='create_case'),

    path('logout', views.logout_user, name='logout'),
    

    path('lawyer/complete-profile/', views.complete_lawyer_profile, name='complete_lawyer_profile'),
    path('client/complete-profile/', views.complete_client_profile, name='complete_client_profile'),

    path('register', views.register, name='register'),
    path('documents/', views.list_documents, name='list_documents'),
    path('download/<file_id>/', views.download_document, name='download_document'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
