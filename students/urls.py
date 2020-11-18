from django.urls import path, include
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_register, name='student_register'),
    path('list/', views.student_list, name='student_list'),
]
