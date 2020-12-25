from django.urls import path, include
from managements import views

app_name = 'managements'

urlpatterns = [
    path('',views.main_page, name="main_page"),
    path('rent/', views.rent, name="rent"),
    path('rent/search_ajax/', views.rent_search_ajax, name='rent_search_ajax'), # 학생 정보 조회 출력
    path('rent/rent_overlap_check/', views.rent_overlap_check, name='rent_overlap_check'),# 대여중인 기자재 중복 검사
    path('rent/rent_list', views.rent_list, name="rent_list"),
    path('return/', views.return_, name="return_"),
    path('return/return_result/<int:pk>', views.return_result, name='return_result'),
    path('return/return_list/', views.return_list, name="return_list"),
    path('return/return_info/', views.return_, name="return_info"),
]
