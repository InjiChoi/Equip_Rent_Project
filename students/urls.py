from django.urls import path, include
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_register, name='student_register'),
    path('list/', views.student_list, name='student_list'),
    path('list/list_search/', views.list_search, name='list_search'),
    path('student_check/', views.student_overlap_check, name='student_overlap_check'),
    path('detail/<int:pk>/',views.student_detail, name='student_detail'),
    path('remove/<int:pk>/',views.student_remove, name='student_remove'),
]
