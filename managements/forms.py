from django import forms
from managements.models import RentManage
from students.models import Student
from equipments.models import Equipment

class RentForm(forms.ModelForm):
    class Meta:
        model = RentManage
        fields = ('equip_pic',)

class RentStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_id', 'phone_number', 'email',)

class RentEquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ('equip_id','equip_type',)
