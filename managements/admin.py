from django.contrib import admin
from managements.models import RentManage, ReturnHistory, Equip_Picture
# Register your models here.
@admin.register(RentManage)
class RentManageAdmin(admin.ModelAdmin):
    list_display=('student', 'equip','rent_date',)

@admin.register(Equip_Picture)
class EquipPictureAdmin(admin.ModelAdmin):
    list_display=('rent', 'equip_pic',)

@admin.register(ReturnHistory)
class ReturnHistoryAdmin(admin.ModelAdmin):
    list_display=('student', 'equip', 'return_date',)