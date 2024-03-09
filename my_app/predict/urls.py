from django.urls import path
from .import views

app_name = "predict"

urlpatterns =[
    path('', views.login_user, name='login'),
    path('lawyer_dashboard/', views.lawyer_data, name='lawyer_dashboard'),
    path('client_dashboard/', views.client_data, name='client_dashboard'),
    path('lawyer/', views.lawyer_data, name='lawyer_data_input'),
    path('lawyer_data/', views.lawyer_data_input, name='lawyer_data_entry'),
    path('client/', views.client_data, name='client_data_input'),
    path('client_data/', views.client_data_input, name='client_data_entry'),
    path('case/', views.case_data, name='case_data_input'),
    path('case_data/', views.case_data_input, name='case_data_entry'),
    path('home/', views.predict, name='prediction_page'),
    path('predict/', views.predict_chances, name='submit_prediction'),
    path('results/', views.view_results, name='results'),
]