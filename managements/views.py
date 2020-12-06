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
                                # rent_info.student = Student.objects.get(id=rent_student[0]).student_id
                                rent_info.equip = rent_equipment[0]
                                rent_info.rent_date = timezone.now()
                                rent_info.save()

                        else:
                                print(10)

                        return redirect('managements:rent_list')

                except IntegrityError:
                        print('integrityerror')
                        rent_form = RentForm()
                        rent_student_form = RentStudentForm()
                        rent_equipment_form = RentEquipmentForm()
                        return render(request, 'managements/rent.html', {'rent_form':rent_form, 'rent_student_form':rent_student_form, 'rent_equipment_form':rent_equipment_form})
        else:
                print('get')
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
        #         # return_form = ReturnForm(request.POST)
        #         # print(1)
        #         # if return_form.is_valid():
        #         #         print(2)
        #         #         return_info = ReturnHistory(**return_form.cleaned_data)
        #         #         # return_info = return_form.save(commit=False)
        #         #         # return_info.student = request.POST.get('return_student')
        #         #         # return_info.equip = request.POST.get('return_equip')
        #         #         # return_info.return_date = timezone.now()
        #         #         return_info.save
        #         #         print(return_info)

        #         #         # ctx = {
        #         #         #         'return_info':return_info,
        #         #         # }
        #         #         # return render(request, 'managements/return_result.html', ctx)
        # # else:
        # print(return_form.return_equipment)
        if request.method =='POST':
                equip_id = request.POST.get('equip_id')
                student_id = request.POST.get('student_id')
                student = get_object_or_404(Student, student_id=student_id)
                equip = get_object_or_404(Equipment,equip_id=equip_id)
                # rent = get_object_or_404(RentManage,student=student_id)

                ctx = {
                        'student':student,
                        'equip':equip,

                }

                return render(request,'managements/return_info.html',ctx)

        else : 
                return_form = ReturnForm()
                ctx = {
                        'return_form':return_form
                }

                return render(request, 'managements/return.html', ctx)

def return_info(request):
        rents = RentManage.objects.all()
        
        ctx = {
        'rents':rents
        }
        return render(request, 'managements/rent_list.html', ctx)
                


def return_result(request):
        return render(request, 'managements/return_result.html')

def return_list(request):
        returns = ReturnHistory.objects.all()
        students = Student.objects.all()
        equipments = Equipment.objects.all()

        ctx = {
                'returns':returns,
                'students':students,
                'equipments':equipments
        }
        return render(request, 'managements/return_list.html')