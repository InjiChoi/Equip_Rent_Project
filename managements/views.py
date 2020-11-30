from django.shortcuts import render, redirect, get_object_or_404
from .models import RentManage, ReturnHistory
from students.models import Student
from equipments.models import Equipment
from managements.forms import RentForm, RentStudentForm, RentEquipmentForm, ReturnForm
from students.models import Student
from equipments.models import Equipment
from django.utils import timezone
from django.db import IntegrityError
from django.contrib import messages



def main_page(request):
    return render(request, 'managements/main.html',{})

# 대여 페이지
def rent(request):
        if request.method == 'POST':
                try : 
                        rent_student = Student.objects.get_or_create(
                                student_id=request.POST.get('student_id'), 
                                name=request.POST.get('name'),
                                phone_number=request.POST.get('phone_number'),
                                email=request.POST.get('email'))
                        rent_equipment = Equipment.objects.get_or_create(
                                equip_id=request.POST.get('equip_id'),
                                equip_type=request.POST.get('equip_type'),
                                rent_status=True,
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
                                rent_info.student = rent_student[0]
                                rent_info.equip = rent_equipment[0]
                                rent_info.rent_date = timezone.now()
                                rent_info.save()

                        else:
                                print(10)

                        return redirect('managements:rent_list') #view-name이용

                except IntegrityError:
                        rent_form = RentForm()
                        rent_student_form = RentStudentForm()
                        rent_equipment_form = RentEquipmentForm()
                        return render(request, 'managements/rent.html', {'rent_form':rent_form, 'rent_student_form':rent_student_form, 'rent_equipment_form':rent_equipment_form})
        else:
                rent_form = RentForm()
                rent_student_form = RentStudentForm()
                rent_equipment_form = RentEquipmentForm()
                ctx = {
                        'rent_form':rent_form,
                        'rent_student_form':rent_student_form,
                        'rent_equipment_form':rent_equipment_form
                }
                return render(request, 'managements/rent.html', ctx)

def rent_list(request):
        rents = RentManage.objects.all()
        
        ctx = {
        'rents':rents
        }
        return render(request, 'managements/rent_list.html', ctx)
# ----------------------------------------------------------------------- #

# 반납 페이지
def return_(request):
        # if request.method == 'POST':
        #         return_form = ReturnForm(request.POST)
        #         if return_form.is_valid():
        #                 return_info = return_form.save(commit=False)
        #                 return_info.

        # else:
        #         return_form = ReturnForm()

        return render(request, 'managements/return.html')

def return_list(request):
        # returns = ReturnHistory.objects.all()
        # students = Student.objects.all()
        # equipments = Equipment.objects.all()

        # ctx = {
        #         'rents':rents,
        #         'students':students,
        #         'equipments':equipments
        # }
        return render(request, 'managements/return_list.html')