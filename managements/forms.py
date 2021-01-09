from django import forms
from managements.models import RentManage, ReturnHistory


# 대여 폼
class RentForm(forms.ModelForm):
        class Meta:
                model = RentManage
                exclude = ['student', 'equip', 'rent_date',]

# 반납 폼
class ReturnForm(forms.Form):
        return_student = forms.CharField(max_length=100)
        return_equipment = forms.CharField(max_length=100)
        return_date = forms.DateTimeField()
