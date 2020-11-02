from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
# from .models import RentManage
from managements.forms import RentForm, RentStudentForm, RentEquipmentForm
# Create your views here.

def rent(request):
        return render(request, 'managements/rent.html', {})

# def rent_list(request):
#     return render(request, 'managements/rent.html')


def main_page(request):
    return render(request, 'managements/main.html',{})