from django import forms
from django.forms import HiddenInput
from managements.models import RentManage, ReturnHistory
from students.models import Student
from equipments.models import Equipment

# 대여 폼
class RentForm(forms.ModelForm):
        class Meta:
                model = RentManage
                exclude = ['student', 'equip', 'rent_date',]
                
class RentStudentForm(forms.ModelForm):
        class Meta:
                model = Student
                fields = ('student_id', 'name', 'phone_number', 'email',)

class RentEquipmentForm(forms.ModelForm):
        class Meta:
                model = Equipment
                fields = ('equip_id','equip_type',)


# 반납 폼
class ReturnForm(forms.Form):
        return_student = forms.CharField(max_length=100)
        return_equipment = forms.CharField(max_length=100)
        return_date = forms.DateTimeField()
