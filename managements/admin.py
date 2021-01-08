from django.contrib import admin
from managements.models import RentManage, ReturnHistory
# Register your models here.
@admin.register(RentManage)
class RentManageAdmin(admin.ModelAdmin):
    list_display=('student', 'equip','rent_date',)

@admin.register(ReturnHistory)
class ReturnHistoryAdmin(admin.ModelAdmin):
    list_display=('student', 'equip', 'return_date',)