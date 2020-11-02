from django.urls import path, include
from managements import views

app_name = 'managements'

urlpatterns = [
    path('', views.rent, name="rent"),
]
