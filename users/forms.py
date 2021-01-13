from django import forms
from django.contrib.auth.models import User
from django.contrib import auth

class StaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password',)