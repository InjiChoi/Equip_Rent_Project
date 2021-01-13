from django.db import models
from students.models import Student
from equipments.models import Equipment


class RentManage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rent_students',null=True)
    equip = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='rent_equip',null=True)
    rent_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def publish(self):
        self.rent_date = timezone.now()
        self.save()

class Equip_Picture(models.Model):
    equip_pic = models.ImageField(upload_to="equip_pic/%Y/%m/%d/", default=None)
    rent = models.ForeignKey(RentManage, on_delete=models.CASCADE)


class ReturnHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    equip= models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)
    return_date = models.DateTimeField(blank=True, null=True)


# 반납 보류 모델 추가
class PendingHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    equip= models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)
    reason = models.TextField()
    pending_date = models.DateTimeField(auto_now_add=True)

class PendingEquipPicture(models.Model):
    pending_equip_pic = models.ImageField(upload_to="pending_equip_pic/%Y/%m/%d/", default=None)
    pending = models.ForeignKey(PendingHistory, on_delete=models.CASCADE)