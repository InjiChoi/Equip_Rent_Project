from django.contrib import admin
from managements.models import RentManage, ReturnHistory, Equip_Picture, PendingHistory, PendingEquipPicture
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

@admin.register(PendingHistory)
class PendingHistoryAdmin(admin.ModelAdmin):
    list_display=('student', 'equip', 'reason', 'pending_date',)

@admin.register(PendingEquipPicture)
class PendingEquipPictureAdmin(admin.ModelAdmin):
    list_display=('pending_equip_pic', 'pending',)