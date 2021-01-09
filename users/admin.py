from django.contrib import admin
from users.models import Staff
from django.contrib.auth.models import User

# Register your models here.
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display=('username', 'password')
