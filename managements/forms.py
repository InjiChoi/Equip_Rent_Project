from django import forms
from django.forms import HiddenInput
from managements.models import RentManage
from students.models import Student
from equipments.models import Equipment

class RentForm(forms.ModelForm):
        class Meta:
                model = RentManage
                exclude = ['student_id', 'name', 'equip_id', 'return_date',]
                


class RentStudentForm(forms.ModelForm):
        class Meta:
                model = Student
                fields = ('student_id', 'name', 'phone_number', 'email',)


class RentEquipmentForm(forms.ModelForm):
        class Meta:
                model = Equipment
                fields = ('equip_id','equip_type',)
