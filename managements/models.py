from django.db import models
from students.models import Student
from equipments.models import Equipment

class RentManage(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rent_students',null=True)
    # name = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rent_name',null=True)
    # phone_number = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rent_phone_number',null=True)
    # email = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rentemail',null=True)

    equip_id = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='rent_equip_id',null=True)
    # equip_type = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='rent_equip_type',null=True)
    equip_pic = models.ImageField(upload_to="equip_pic/%Y/%m/%d/")




class ReturnHistory(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    equip_id = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)

    return_date = models.DateTimeField(auto_now_add=True)