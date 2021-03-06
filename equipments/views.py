from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Equipment
from managements.models import RentManage
from students.models import Student
from .forms import EquipForm
from django.contrib import messages
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django import forms
from django.core.validators import FileExtensionValidator
from django.db import IntegrityError
import xlwt

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

# 기자재 excel 한꺼번에 등록
class UploadFileForm(forms.Form):
    file = forms.FileField()

@login_required(login_url='/users/')
def equip_excel_register(request):
    if request.method == "POST":
        try:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                request.FILES['file'].save_to_database(
                    name_columns_by_row=0, # 첫 번째 행 제목
                    model=Equipment,
                    mapdict=['equip_id', 'equip_type'])
                return redirect('equipments:equipment_list')
            else:
                return redirect('equipments:equip_excel_register')
        except IntegrityError:
            return redirect('equipments:equip_excel_register')
    else:
        form = UploadFileForm()
    return render(request, 'equipments/equip_excel_register.html', {'form': form})

# 기자재 리스트 엑셀 export
@login_required(login_url='/users/')
def equip_excel_download(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="equipments.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Equipments')
    row_num = 0 # sheet header
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['물품번호', '물품종류', '대여상태']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    
    rows = Equipment.objects.all().values_list('equip_id', 'equip_type', 'rent_status')
    for row in rows :
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    
    wb.save(response)
    return response

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
    equip = Equipment.objects.all().order_by('-id')
    paginator = Paginator(equip, 10)
    page = request.GET.get('page')
    rents = RentManage.objects.all()
    equipments = paginator.get_page(page)
    ctx = {
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

    search_list = search_list.order_by('-id')
    paginator = Paginator(search_list, 10)
    page = request.GET.get('page')
    equipments = paginator.get_page(page)
    
    ctx = {
        'equipments':equipments,
        'rents':rents,
    }
    return render(request, 'equipments/equip_list_search_1.html', ctx)

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

    search_list = search_list.order_by('-id')
    paginator = Paginator(search_list, 10)
    page = request.GET.get('page')
    equipments = paginator.get_page(page)

    ctx = {
            "equipments":equipments,
            "rents":rents,
    }

    return render(request, 'equipments/equip_list_search_2.html', ctx)

