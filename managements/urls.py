from django.urls import path, include
from managements import views

app_name = 'managements'

urlpatterns = [
    path('',views.main_page, name="main_page"),
    path('rent/', views.rent, name="rent"),
    path('rent/search/', views.lookup_student, name="lookup_student"),
    path('rent/rent_overlap_check/', views.rent_overlap_check, name='rent_overlap_check'),# 대여중인 기자재 중복 검사
    path('rent/rent_list/', views.rent_list, name="rent_list"),
    path('rent/rent_list/search_rent_list/', views.search_rent_list, name="search_rent_list"),
    path('rent/rent_list/search_rent_pledge/', views.search_rent_pledge, name="search_rent_pledge"),
    path('return/', views.return_, name="return_"),
    path('return/return_exist_check/', views.return_exist_check, name='return_exist_check'),# 반납 시 대여 리스트에 있는지 검사
    path('return/return_result/<int:pk>/', views.return_result, name='return_result'),
    path('return/return_list/', views.return_list, name="return_list"),
    path('return/return_list/search_return_list/', views.search_return_list, name="search_return_list"),
    path('return/return_info/', views.return_, name="return_info"),
    path('rent/activate/<int:pk>/', views.activate, name="activate"),
]
