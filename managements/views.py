from django.shortcuts import render, redirect, get_object_or_404
from .models import RentManage
from managements.forms import RentForm, RentStudentForm, RentEquipmentForm
from students.models import Student
from equipments.models import Equipment
# from django.db import transaction
# Create your views here.

def rent(request):
        if request.method == 'POST':
                rent_student = Student.objects.get_or_create(
                        student_id=request.POST.get('student_id'), 
                        name=request.POST.get('name'),
                        phone_number=request.POST.get('phone_number'),
                        email=request.POST.get('email'))
                rent_equipment = Equipment.objects.get_or_create(
                        equip_id=request.POST.get('equip_id'),
                        equip_type=request.POST.get('equip_type'),
                )
                rent_form = RentForm(request.POST, request.FILES)
                # rent_student_form = RentStudentForm(request.POST)
                # rent_equipment_form = RentEquipmentForm(request.POST)
                print(0)
                if rent_form.is_valid() :
                        print(55)
                        # rent_student = rent_student_form.save()
                        # rent_equipment_form.save()
                        rent_info = rent_form.save(commit=False)
                        rent_info.student_id = rent_student[0]
                        rent_info.equip_id = rent_equipment[0]
                        # rent_info.name = rent_obj[1]
                        rent_info.save()

                        print(1)
                        
                        print(2)
                else:
                        print(10)

                return render(request, 'managements/main.html',{})
        else:
                print(4)
                rent_form = RentForm()
                rent_student_form = RentStudentForm()
                rent_equipment_form = RentEquipmentForm()
                return render(request, 'managements/rent.html', {'rent_form':rent_form, 'rent_student_form':rent_student_form, 'rent_equipment_form':rent_equipment_form})

def main_page(request):
    return render(request, 'managements/main.html',{})