from django.shortcuts import render, redirect, get_object_or_404
from .models import RentManage
from managements.forms import RentForm
# Create your views here.

def rent(request):
        if request.method == 'POST':
                # student = Student.objects.get(id=pk)
                rent_form = RentForm(request.POST, request.FILES)
                equip_pic = request.POST['equip_pic']
                print(0)
                if rent_form.is_valid():
                        print(55)
                        info = RentManage(equip_pic=rent_form.data['equip_pic'])
                        # rent_info = rent_form.save(commit=False)
                        print(1)
                        info.save()
                        print(2)
                else:
                        print(10)

                return render(request, 'managements/rent.html', {'rent_form':rent_form} )
        else:
                
                print(4)
                rent_form = RentForm()

                return render(request, 'managements/rent.html', {'rent_form':rent_form})
