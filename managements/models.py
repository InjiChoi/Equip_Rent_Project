from django.db import models
from students.models import Student
from equipments.models import Equipment

class RentManage(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rent_students')
    name = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rent_name')
    phone_number = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rent_phone_number')
    email = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rentemail')

    equip_id = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='rent_equip_id')
    equip_type = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='rent_equip_type')
    equip_pic = models.ImageField(upload_to="equip_pic/%Y/%m/%d/")

    # rent_id = models.PositiveIntegerField(default=0)
    return_date = models.DateTimeField(null=True, blank=True)


