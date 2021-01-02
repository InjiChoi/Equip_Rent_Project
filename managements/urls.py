from django.urls import path, include
from managements import views

app_name = 'managements'

urlpatterns = [
    path('',views.main_page, name="main_page"),
    path('rent/', views.rent, name="rent"),
    path('rent/search/', views.lookup_student, name="lookup_student"),
    path('rent/rent_overlap_check/', views.rent_overlap_check, name='rent_overlap_check'),# 대여중인 기자재 중복 검사
    path('rent/rent_list/', views.rent_list, name="rent_list"),
    path('return/', views.return_, name="return_"),
    path('return/return_result/<int:pk>/', views.return_result, name='return_result'),
    path('return/return_list/', views.return_list, name="return_list"),
    path('return/return_list/list_search/', views.list_search, name="list_search"),
    path('return/return_info/', views.return_, name="return_info"),
]
