from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from .models import Equipment
from .forms import EquipForm
from django.contrib import messages

# Create your views here.
def equipment_register(request):
    if request.method == 'POST':
        equipment_form = EquipForm(request.POST)
        if equipment_form.is_valid():
            equip_info = equipment_form.save(commit=False)
            equip_info.save()
        else :
            messages.info(request,"중복된 사항으로 기자재 등록에 실패했습니다.")

        return render(request, 'equipments/equipment_register.html')
    else:
        equipment_form = EquipForm()
        return render(request, 'equipments/equipment_register.html', {'equipment_form':equipment_form})
