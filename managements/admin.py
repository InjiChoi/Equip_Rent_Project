from django.contrib import admin
from managements.models import RentManage
# Register your models here.
@admin.register(RentManage)
class RentManageAdmin(admin.ModelAdmin):
    list_display=('student_id', 'name', 'phone_number', 'email',
                    'equip_id', 'equip_type', 'equip_pic', 'return_date')