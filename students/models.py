from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    status = models.SmallIntegerField(default=0)
