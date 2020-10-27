from django.db import models

class Equipment(models.Model):
    equip_id = models.CharField(max_length=255)
    equip_type = models.SmallIntegerField(default=0)
    rent_status = models.BooleanField(default=False)