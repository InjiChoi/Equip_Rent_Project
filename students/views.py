from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

# Create your views here.
def student_register(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_info = student_form.save(commit=False)
            student_info.save()
        return render(request, 'students/student_register.html')
    else:
        student_form = StudentForm()
        return render(request, 'students/student_register.html', {'student_form':student_form})

