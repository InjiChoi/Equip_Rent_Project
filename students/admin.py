from django.contrib import admin
from students.models import Student
# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=('student_id', 'name', 'phone_number', 'email', 'status')