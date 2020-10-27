from django.db import models

class RentManage(models.Model):
    rent_id = models.PositiveIntegerField(default=0)
    equip_pic = models.ImageField(upload_to="equip_pic/%Y/%m/%d/")
    return_date = models.DateTimeField(default=None)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    equip_id = models.ForeignKey(Equipment, on_delete=models.CASCADE)
