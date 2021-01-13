from django import forms
from equipments.models import Equipment

class EquipForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ('equip_id', 'equip_type',)