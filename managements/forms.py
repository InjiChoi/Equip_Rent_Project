from django import forms
from django.forms import HiddenInput
from managements.models import RentManage
from students.models import Student
from equipments.models import Equipment

# class RentForm(forms.Form):
#         student_id = forms.CharField(label='대여자 학번')
#         student_name = forms.CharField(label='대여자 이름')
#         phone_number = forms.CharField(label='대여자 핸드폰번호')
#         email = forms.EmailField(label='대여자 email')

#         equip_id = forms.CharField(label='물품 번호')
#         equip_type = forms.ChoiceField(label='물품 종류')

#         equip_pic = forms.ImageField(label='기자재 상태 확인용 사진')

class RentForm(forms.ModelForm):
        class Meta:
                model = RentManage
                exclude = ['student_id', 'name', 'phone_number', 'email','equip_id','equip_type','return_date']
                


class RentStudentForm(forms.ModelForm):
        class Meta:
                model = Student
                fields = ('student_id', 'name', 'phone_number', 'email',)


class RentEquipmentForm(forms.ModelForm):
        class Meta:
                model = Equipment
                fields = ('equip_id','equip_type',)
