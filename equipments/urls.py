from django.urls import path, include
from equipments import views

app_name = 'equipments'

urlpatterns = [
    path('', views.equipment_register, name="equipment_register"),
    path('list/', views.equipment_list, name='equipment_list'),
    path('detail/<int:pk>/',views.equipment_detail, name='equipment_detail'),
]
