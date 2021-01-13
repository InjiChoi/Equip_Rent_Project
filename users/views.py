from django.shortcuts import render, redirect, get_object_or_404
from .forms import StaffForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

#관리자 로그인
@csrf_exempt
def staff_login(request):
    if request.method == 'POST':
        staff_form = StaffForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username = username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('managements:main_page')
        else :
            staff_form = StaffForm()
            return render(request, 'users/staff_login.html', {'staff_form':staff_form})

    else:
        staff_form = StaffForm()
        return render(request, 'users/staff_login.html', {'staff_form':staff_form})

#로그인 성공 여부에 따른 alert
@csrf_exempt
def login_success_check(request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = auth.authenticate(request, username = username,password=password)

        if user is not None: #사용자 존재
            u_exist = "pass"
        elif user is None :  #사용자 존재x
            u_exist="fail"
        
        ctx = {
            'u_exist':u_exist
        }

        return JsonResponse(ctx)
    
#관리자 로그아웃
def staff_logout(request):
    auth.logout(request)
    staff_form = StaffForm()
    return redirect('managements:main_page')
