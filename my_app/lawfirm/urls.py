from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_user, name="login"),
    path('lawyer_dashboard/<int:lawyer_id>/', views.lawyer_dashboard, name='lawyer_dashboard'),
    #path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register, name='register_user'),
]