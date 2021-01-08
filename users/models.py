from django.db import models
from django.contrib.auth.models import User

class Staff(User):
    nickname = models.CharField(max_length=30)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)