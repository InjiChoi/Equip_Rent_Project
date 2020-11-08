from django.urls import path, include
from managements import views

app_name = 'managements'

urlpatterns = [
    path('',views.main_page, name="main_page"),
    path('rent/', views.rent, name="rent"),
    path('rent/rent_list', views.rent_list, name="rent_list")
]
