from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from .models import Equipment
from managements.models import RentManage
from students.models import Student
from .forms import EquipForm

# Create your views here.
def equipment_register(request):
    if request.method == 'POST':
        equipment_form = EquipForm(request.POST)
        if equipment_form.is_valid():
            equip_info = equipment_form.save(commit=False)
            equip_info.save()
        return render(request, 'equipments/equipment_register.html')
    else:
        equipment_form = EquipForm()
        return render(request, 'equipments/equipment_register.html', {'equipment_form':equipment_form})

def equipment_list(request):
    equipments = Equipment.objects.all()

            
    ctx = {
        'equipments':equipments
    }
    return render(request, 'equipments/equipment_list.html', ctx)