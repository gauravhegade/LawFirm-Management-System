from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


app_name = 'lawyer_app'

urlpatterns = [
    path('', views.info ,name='home'),
    path('login', views.login_user, name='login'),
    path('upload-document', views.upload_document, name='upload_document'),
    path('lawyer/case-status', views.case_status, name='case_status'),
    path('client/dashboard', views.client_dashboard, name='client_dashboard'),

    path('client/<int:client_id>', views.client_profile, name='client_profile'),
    path('lawyer/<int:lawyer_id>', views.lawyer_profile, name='lawyer_profile'),

    path('client/approve-case', views.approve_case, name='approve_case'),
    path('search-clients', views.search_clients, name='search_clients'),
    path('search-cases', views.search_cases, name='search_cases'),

    path('lawyer/dashboard', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('lawyer/create-case', views.create_case, name='create_case'),

    path('logout', views.logout_user, name='logout'),
    

    path('lawyer/complete-profile', views.complete_lawyer_profile, name='complete_lawyer_profile'),
    path('client/complete-profile', views.complete_client_profile, name='complete_client_profile'),

    path('register', views.register, name='register'),

     path('predict/', views.predict, name='predict'),
    path('predict_results/', views.predict_chances, name='predict_chances'),
    path('submit_prediction/', views.predict_chances, name='submit_prediction'),
    #path('documents/', views.list_documents, name='list_documents'),
    #path('documents-case/<int:case_id>', views.list_documents_by_case, name='list_documents_by_case'),
    path('documents/download/<str:file_id>', views.download_document, name='download_document'),
    path('documents/view/<str:file_id>', views.view_document, name='view_document'),
    path('cases/<int:case_id>', views.case_details, name='case_details'),
    path('documents/cases/<int:case_id>', views.fetch_case_documents, name='fetch_case_documents'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
