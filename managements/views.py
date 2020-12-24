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
                rent_student_id = request.POST.get('student_id')
                rent_equipment_id = request.POST.get('equip_id')
                print(rent_student_id)
                # rent_student = Student.objects.get(student_id=rent_student_id)
                rent_student = get_object_or_404(Student, student_id=rent_student_id)
                rent_equip = get_object_or_404(Equipment, equip_id=rent_equipment_id)

                rent_form = RentForm(request.POST, request.FILES)
                if rent_form.is_valid() :
                        rent_info = rent_form.save(commit=False)
                        rent_info.student = rent_student
                        rent_info.equip = rent_equip
                        rent_info.rent_date = timezone.now()
                        rent_equip.rent_status = True
                        rent_equip.save()
                        rent_info.save()
                return redirect('managements:rent_list')
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

# 학생 정보 조회
def rent_search_ajax(request):
        print(1)
        dict={'test':'json_sample'}
        return HttpResponse(json.dumps(dict), content_type='application/json')


def rent_list(request):
        rents = RentManage.objects.all()
        
        ctx = {
        'rents':rents
        }
        return render(request, 'managements/rent_list.html', ctx)
# ----------------------------------------------------------------------- #

# 반납 페이지
def return_(request):
        if request.method =='POST':
                equip_id = request.POST.get('equip_id')
                student_id = request.POST.get('student_id')
                student = get_object_or_404(Student, student_id=student_id)
                equip = get_object_or_404(Equipment,equip_id=equip_id)
                rent = get_object_or_404(RentManage, equip=equip.pk)

                ctx = {
                        'student':student,
                        'equip':equip,
                        'rent':rent
                }

                return render(request,'managements/return_info.html',ctx)

        else : 
                return_form = ReturnForm()
                ctx = {
                        'return_form':return_form
                }

                return render(request, 'managements/return.html', ctx)
                


def return_result(request, pk):
        rent_equip = Equipment.objects.get(pk=pk)
        rent_equip.rent_status = False
        rent_equip.save()
        rent = RentManage.objects.get(equip = rent_equip)
        rent_student = Student.objects.get(student_id=rent.student.student_id)
        return_instance = ReturnHistory.objects.create(student=rent_student, equip=rent_equip, return_date=timezone.now())
        rent.delete()
        return redirect('managements:return_list')


def return_list(request):
        returns = ReturnHistory.objects.all()

        ctx = {
                'returns':returns
        }
        return render(request, 'managements/return_list.html',ctx)


