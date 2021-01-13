from django.urls import path, include
from equipments import views

app_name = 'equipments'

urlpatterns = [
    path('', views.equipment_register, name="equipment_register"),
    path('list/', views.equipment_list, name='equipment_list'),
    path('list/list_search/', views.list_search, name='list_search'),
    path('equip_check/', views.equipment_overlap_check, name="equipment_overlap_check"),
    path('detail/<int:pk>/',views.equipment_detail, name='equipment_detail'),
    path('remove/<int:pk>/',views.equipment_remove, name='equipment_remove'),
    path('remove/check/', views.equip_remove_check, name='equip_remove_check'),
]
