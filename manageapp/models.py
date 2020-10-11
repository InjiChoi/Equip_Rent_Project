from django.db import models

class Student(models.Model):
    student_id = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    status = models.SmallIntegerField(default=0)

class RentManage(models.Model):
    rent_id = models.PositiveIntegerField(default=0)
    equip_pic = models.ImageField(upload_to="equip_pic/%Y/%m/%d/")
    return_date = models.DateTimeField(default=None)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    equip_id = models.ForeignKey(Equipment, on_delete=models.CASCADE)

class Equipment(models.Model):
    equip_id = models.CharField(max_length=255)
    equip_type = models.SmallIntegerField(default=0)
    rent_status = models.BooleanField(default=False)