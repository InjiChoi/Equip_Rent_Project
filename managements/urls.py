from django.urls import path, include
from managements import views

app_name = 'managements'

urlpatterns = [
    path('',views.main_page, name="main_page"),
    path('rent/', views.rent, name="rent"),
]
