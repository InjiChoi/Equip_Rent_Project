from django.urls import path, include
from . import views

app_name = "users"

urlpatterns=[
    path('', views.staff_login, name="staff_login"), 
    path('users/login_check', views.login_success_check, name="login_success_check"), 
    path('logout/', views.staff_logout, name="staff_logout"), 
]