from django.contrib import admin
from managements.models import RentManage, ReturnHistory
# Register your models here.
@admin.register(RentManage)
class RentManageAdmin(admin.ModelAdmin):
    list_display=('student_id', 'equip_id', 'equip_pic',)

@admin.register(ReturnHistory)
class ReturnHistoryAdmin(admin.ModelAdmin):
    list_display=('student_id', 'equip_id', 'return_date',)