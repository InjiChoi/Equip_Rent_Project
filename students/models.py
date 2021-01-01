from django.db import models

# Create your models here.
class Student(models.Model):

    STATUS_CHOICES = (
        ('재학', '재학'),
        ('휴학', '휴학'),
        ('졸업', '졸업'),
        ('자퇴', '자퇴'),
    )

    student_id = models.CharField(max_length=7, unique=True)
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='재학')

    def __str__(self):
        return self.student_id


