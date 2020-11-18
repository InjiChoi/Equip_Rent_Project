from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib import messages

# Create your views here.
def student_register(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_info = student_form.save(commit=False)
            student_info.save()
        else :
            messages.info(request,"중복된 사항으로 학생 등록에 실패했습니다.")

        return render(request, 'students/student_register.html')
    else:
        student_form = StudentForm()
        return render(request, 'students/student_register.html', {'student_form':student_form})

def student_list(request):
    students = Student.objects.all()

    ctx = {
        'students':students,
    }
    return render(request, 'students/student_list.html', ctx)

