from django.urls import path, include
from equipments import views

app_name = 'equipments'

urlpatterns = [
    path('', views.equipment_register, name="equipment_register"),
    path('list/', views.equipment_list, name='equipment_list'),
]
