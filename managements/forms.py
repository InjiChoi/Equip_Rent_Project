from django import forms
from django.forms import HiddenInput
from managements.models import RentManage, ReturnHistory, Equip_Picture


# 대여 폼
class RentForm(forms.ModelForm):
        class Meta:
                model = RentManage
                exclude = ['student', 'equip', 'rent_date',]

class EquipPictureForm(forms.ModelForm):
        class Meta:
                model = Equip_Picture
                fields = ('equip_pic',)
                



# 반납 폼
class ReturnForm(forms.Form):
        return_student = forms.CharField(max_length=100)
        return_equipment = forms.CharField(max_length=100)
        return_date = forms.DateTimeField()
