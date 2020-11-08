from django.shortcuts import render, redirect, get_object_or_404
from .models import RentManage
from managements.forms import RentForm, RentStudentForm, RentEquipmentForm
from students.models import Student
from equipments.models import Equipment
# from django.db import transaction
# Create your views here.

# class rent(FromView):
#         template_name = 'rent.html'
#         form_class = RentForm
#         success_url = '/'
#         def from_valid(self, form):
#                 with transaction.atomic():


def rent(request):
        if request.method == 'POST':
                rent_form = RentForm(request.POST, request.FILES)
                rent_student_form = RentStudentForm(request.POST)
                rent_equipment_form = RentEquipmentForm(request.POST)

                print(0)
                if rent_form.is_valid() and rent_student_form.is_valid() and rent_equipment_form.is_valid():
                        print(55)
                        # rent_info = rent_form.save(commit=False)
                        student_info = rent_student_form.save(commit=False)
                        equip_info = rent_equipment_form.save(commit=False)
                        print(1)
                        # rent_info.save()
                        student_info.save()
                        equip_info.save()
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