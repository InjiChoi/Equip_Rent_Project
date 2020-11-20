from django.db import models

class Equipment(models.Model):
    TYPE_NOTEBOOK = 'laptop'
    TYPE_TABLET = 'tablet'
    TYPE_SENSOR = 'sensor'
    EQUIP_TYPE_CHOICES = (
        (TYPE_NOTEBOOK,'노트북'),
        (TYPE_TABLET, '태블릿'),
        (TYPE_SENSOR, '센서'),
    )
    equip_id = models.CharField(unique=True,max_length=255)
    equip_type = models.CharField(max_length=20, choices = EQUIP_TYPE_CHOICES, null=True, blank=True)
    rent_status = models.BooleanField(default=False)

    def __str__(self):
        return self.equip_id