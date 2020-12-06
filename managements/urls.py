from django.urls import path, include
from managements import views

app_name = 'managements'

urlpatterns = [
    path('',views.main_page, name="main_page"),
    path('rent/', views.rent, name="rent"),
    path('rent/rent_list', views.rent_list, name="rent_list"),
    path('return/', views.return_, name="return_"),
    path('return/return_result/', views.return_result, name='return_result'),
    path('return/return_list/', views.return_list, name="return_list"),
]
