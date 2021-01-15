from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Equipment
from managements.models import RentManage
from students.models import Student
from .forms import EquipForm
from django.contrib import messages
import json
from django.http import JsonResponse, HttpResponse
from math import ceil
from django.contrib.auth.decorators import login_required

@login_required(login_url='/users/')
def equipment_register(request):
    if request.method == 'POST':
        equipment_form = EquipForm(request.POST)
        if equipment_form.is_valid():
            equip_info = equipment_form.save(commit=False)
            equip_info.save()
            return redirect('equipments:equipment_list')
        else :
            return redirect('equipments:equipment_register')
        
    else:
        equipment_form = EquipForm()
        return render(request, 'equipments/equipment_register.html', {'equipment_form':equipment_form})

# 기자재 물품 번호 중복 확인
@login_required(login_url='/users/')
def equipment_overlap_check(request):
    equip_id = request.GET.get('equip_id')
    try:
        # 중복 검사 실패
        equip = Equipment.objects.get(equip_id=equip_id)
    except:
        # 중복 검사 성공
        equip = None
    if equip is None:
        overlap = "pass"
    else:
        overlap = "fail"
    ctx = {'overlap':overlap}

    return JsonResponse(ctx)

# 기자재 리스트 페이지
@login_required(login_url='/users/')
def equipment_list(request):
    page = int(request.GET.get('page', 1))
    page_size =10
    limit = page_size * page
    offset = limit - page_size
    equipments_count = Equipment.objects.all().count()
    equipments = Equipment.objects.all()[offset:limit]
    page_total = ceil(equipments_count/page_size)
    rents = RentManage.objects.all()
    if page_total == 0:
                page_total += 1
                
    ctx = {
        "page": page,
        "page_total": page_total,
        "page_range": range(1, page_total),
        'equipments': equipments,
        'rents':rents,
    }
    return render(request, 'equipments/equipment_list.html', ctx)

@login_required(login_url='/users/')
def equipment_detail(request, pk):
    equipments = Equipment.objects.all()
    rents = RentManage.objects.all()
    ctx = {
        'equipments':equipments,
        'rents':rents,
    }
    equip = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        form = EquipForm(request.POST, instance=equip)
        if form.is_valid():
            equip = form.save(commit=False)
            equip.equip_id = request.POST.get('equip_id')
            equip.equip_type = request.POST.get('equip_type')
            equip.save()
            return redirect('equipments:equipment_list')
    
    else:
        form = EquipForm(instance=equip)
    return render(request,'equipments/equipment_detail.html',{'form':form})

# 기자개 정보 삭제 페이지
@login_required(login_url='/users/')
def equipment_remove(request, pk):
    equipments = Equipment.objects.all()
    rents = RentManage.objects.all()
    ctx = {
        'equipments':equipments,
        'rents':rents,
    }
    equip = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        if equip.rent_status == 'impossible' or equip.rent_status == 'pending':
            return redirect('equipments:equipment_list')
        elif equip.rent_status == 'possible':
            equip.delete()
            return redirect('equipments:equipment_list')
    
    else:
        form = EquipForm(instance=equip)
    return render(request,'equipments/equipment_remove.html',{'form':form})

@login_required(login_url='/users/')
def equip_remove_check(request):
    equip_id = request.GET.get('equip_id')
    equip = Equipment.objects.get(equip_id=equip_id)
    if equip.rent_status == 'possible':
        remove="pass"
    else:
        remove="fail"
    ctx = {'remove':remove}
    return JsonResponse(ctx)

@login_required(login_url='/users/')
def list_search(request):
    selected_equip_id = request.GET.get('search_input')
    selected_equip_type = request.GET.get('search_select')
    rents = RentManage.objects.all()
    if selected_equip_type == "":
        selected_equip_type = False
    
    if selected_equip_id and selected_equip_type:
        search_list = Equipment.objects.all().filter(equip_id__contains=selected_equip_id, equip_type__contains=selected_equip_type)

    elif selected_equip_id:
        search_list = Equipment.objects.all().filter(equip_id__contains=selected_equip_id)

    elif selected_equip_type:
        search_list = Equipment.objects.all().filter(equip_type__contains=selected_equip_type)

    else:
        search_list = Equipment.objects.all()
    ctx = {
        'search_list':search_list,
        'rents':rents,
    }

    return render(request, 'equipments/lookup_equip_list.html', ctx)

#기자재 리스트에서 대여 상태(rent_status) 검색하는 뷰
@login_required(login_url='/users/')
def search_rent_status(request):
        search_status = request.GET.get('search_status')
        rents = RentManage.objects.all()

        if search_status =="":
                search_status = None
        
        if search_status is not None:
                search_list = Equipment.objects.all().filter(rent_status=search_status)
        else:
                search_list = Equipment.objects.all()

        ctx = {
                "search_list":search_list,
                "rents":rents
        }

        return render(request, 'equipments/lookup_equip_list.html', ctx)
