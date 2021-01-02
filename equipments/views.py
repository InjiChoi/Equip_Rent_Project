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
# Create your views here.
def equipment_register(request):
    if request.method == 'POST':
        equipment_form = EquipForm(request.POST)
        if equipment_form.is_valid():
            equip_info = equipment_form.save(commit=False)
            equip_info.save()
            return redirect('equipments:equipment_list')
            # messages.success(request, "기자재 등록에 성공하였습니다!")
        else :
            return redirect('equipments:equipment_register')
        #     messages.error(request,"중복된 사항으로 기자재 등록에 실패했습니다.")
        
    else:
        equipment_form = EquipForm()
        return render(request, 'equipments/equipment_register.html', {'equipment_form':equipment_form})

# 기자재 물품 번호 중복 확인
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
def equipment_list(request):
    page = int(request.GET.get('page', 1))
    page_size =10
    limit = page_size * page
    offset = limit - page_size
    equipments_count = Equipment.objects.all().count()
    equipments = Equipment.objects.all()[offset:limit]
    page_total = ceil(equipments_count/page_size)
    rents = RentManage.objects.all()

    ctx = {
        "page": page,
        "page_total": page_total,
        "page_range": range(1, page_total),
        'equipments': equipments,
        'rents':rents,
    }
    return render(request, 'equipments/equipment_list.html', ctx)


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
def equipment_remove(request, pk):
    equipments = Equipment.objects.all()
    rents = RentManage.objects.all()
    ctx = {
        'equipments':equipments,
        'rents':rents,
    }
    equip = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        if equip.rent_status:
            return redirect('equipments:equipment_list')
        else:
            equip.delete()
            return redirect('equipments:equipment_list')
    
    else:
        form = EquipForm(instance=equip)
    return render(request,'equipments/equipment_remove.html',{'form':form})

# # 기자재 검색
# def search_equip(request):
#     if request.method == 'POST':
#         selected_equip_id = request.POST.get('selected_equip_id')
#         selected_equip_type = request.POST.get('selected_equip_type')
#         if selected_equip_id == '' and selected_equip_type== '기자재 종류':
#             return redirect('equipments:equipment_list')


#기자재 목록에서 조회하는 뷰
def list_search(request):
    search_key = request.GET.get('search_key') # 검색어 가져오기
    search_list = Equipment.objects.all()

    if search_key: # 만약 검색어가 존재하면
        search_list = search_list.filter(equip_id__contains=search_key)
        rents = RentManage.objects.all()

        ctx = {
                'search_list': search_list,
                'rents':rents
        }
        
        return render(request, 'equipments/lookup_equip_list.html', ctx)