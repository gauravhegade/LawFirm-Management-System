from django.urls import path
from . import views




app_name = 'lawyer_app'

urlpatterns = [
    path('', views.info ,name='home'),
    path('login/', views.login_user, name='login'),

    path('lawyer/case-status/', views.case_status, name='case_status'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),

    path('client/<int:client_id>/', views.client_profile, name='client_profile'),
    path('lawyer/<int:lawyer_id>/', views.lawyer_profile, name='lawyer_profile'),

    path('client/approve-case/', views.approve_case, name='approve_case'),
    path('search-clients/', views.search_clients, name='search_clients'),

    path('lawyer/dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('lawyer/create-case/', views.create_case, name='create_case'),

    path('logout', views.logout_user, name='logout'),
    
   

    path('lawyer/complete-profile/', views.complete_lawyer_profile, name='complete_lawyer_profile'),
    path('client/complete-profile/', views.complete_client_profile, name='complete_client_profile'),

    path('register', views.register, name='register'),
    path('predict/', views.predict, name='predict'),
    
    path('predict_results/', views.predict_chances, name='predict_chances'),
   # path('results/', views.results, name='results'),

    path('submit_prediction/', views.predict_chances, name='submit_prediction'),
    path('documents/',views.index,name='documents')
]

