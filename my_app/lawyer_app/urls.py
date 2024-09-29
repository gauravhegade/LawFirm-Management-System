from django.urls import path
from . import views

app_name = 'lawyer_app'
urlpatterns = [
    path('', views.info ,name='home'),
    path('login/', views.login_user, name="login"),
    #path('lawyer_dashboard/<int:lawyer_id>/', views.lawyer_dashboard, name='lawyer_dashboard'),
    #path('logout_user', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('predict/', views.predict, name='predict'),
    path('predict_results/', views.predict_chances, name='predict_chances'),
   # path('results/', views.results, name='results'),

    path('submit_prediction/', views.predict_chances, name='submit_prediction'),
    path('documents/',views.index,name='documents')
]