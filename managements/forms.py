from django import forms
from managements.models import RentManage
from students.models import Student
from equipments.models import Equipment

# class RentForm(forms.Form):
#         student_id = forms.CharField()
#         student_name = forms.CharField()
#         phone_number = forms.CharField()
#         email = forms.EmailField()
#         equip_id = forms.CharField()
#         equip_type = forms.CharField()
#         equip_pic = forms.ImageField()

class RentForm(forms.ModelForm):
        class Meta:
                model = RentManage
                fields = '__all__'

# class RentStudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ('student_id', 'phone_number', 'email',)

# class RentEquipmentForm(forms.ModelForm):
#     class Meta:
#         model = Equipment
#         fields = ('equip_id','equip_type',)
