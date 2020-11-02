from django.urls import path, include
from managements import views

app_name = 'managements'

urlpatterns = [
    path('', views.rent, name="rent"),
    path('main/',views.main_page, name="main_page")
]
