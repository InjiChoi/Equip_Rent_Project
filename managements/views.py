from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
# from .models import RentManage
from managements.forms import RentForm, RentStudentForm, RentEquipmentForm
# Create your views here.

def rent(request):
    if request.method == 'POST':
        rent_form = RentForm(request.POST)
        rent_student_form = RentStudentForm(request.POST)
        rent_equipment_form = RentEquipmentForm(request.POST)

        if rent_form.is_valid() and rent_student_form.is_valid() and rent_equipment_form.is_valid() :
            rent_info = rent_form.save(commit=False)
            rent_student_info = rent_student_form.save(commit=False)
            rent_equipment_info = rent_equipment_form.save(commit=False)
            rent_info.save()
            rent_student_info.save()
            rent_equipment_info.save()
            return redirect('managements:rent_list')
    else:
        rent_form = RentForm()
        rent_student_form = RentStudentForm()
        rent_equipment_form = RentEquipmentForm()
        ctx = {
            'rent_form':rent_form,
            'rent_student_form':rent_student_form,
            'rent_equipment_form':rent_equipment_form,
        }
        return render(request, 'managements/rent.html', ctx)

# def rent_list(request):
#     return render(request, 'managements/rent.html')