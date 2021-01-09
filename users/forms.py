from django import forms
from .models import Staff
from django.contrib.auth.models import User
from django.contrib import auth

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('username','password',)