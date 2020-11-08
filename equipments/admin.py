from django.contrib import admin
from .models import Equipment
# Register your models here.
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display=('equip_id', 'equip_type', 'rent_status')