from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from .models import Equipment
from managements.models import RentManage
from students.models import Student
from .forms import EquipForm
from django.contrib import messages

# Create your views here.
def equipment_register(request):
    if request.method == 'POST':
        equipment_form = EquipForm(request.POST)
        if equipment_form.is_valid():
            equip_info = equipment_form.save(commit=False)
            equip_info.save()
            messages.success(request, "기자재 등록에 성공하였습니다!")
            
        else :
            messages.error(request,"중복된 사항으로 기자재 등록에 실패했습니다.")

        return render(request, 'equipments/equipment_message.html')
    else:
        equipment_form = EquipForm()
        return render(request, 'equipments/equipment_register.html', {'equipment_form':equipment_form})

def equipment_list(request):
    equipments = Equipment.objects.all()
    rents = RentManage.objects.all()
    ctx = {
        'equipments':equipments,
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
            return render(request, 'equipments/equipment_list.html', ctx)
    
    else:
        form = EquipForm(instance=equip)
    return render(request,'equipments/equipment_detail.html',{'form':form})
