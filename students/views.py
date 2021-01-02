from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib import messages
import json
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from math import ceil

# Create your views here.
def student_register(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_info = student_form.save(commit=False)
            student_info.save()
            return redirect('students:student_list')
        else :
            return redirect('students:student_register')
        #     messages.info(request,"중복된 사항으로 학생 등록에 실패했습니다.")

        return render(request, 'students/student_register.html')
    else:
        student_form = StudentForm()
        return render(request, 'students/student_register.html', {'student_form':student_form})


# 학생 번호 중복 확인
def student_overlap_check(request):
    student_id = request.GET.get('student_id')
    try:
        # 중복 검사 실패
        student = Student.objects.get(student_id=student_id)
    except:
        # 중복 검사 성공
        student = None
    if student is None:
        overlap = "pass"
    else:
        overlap = "fail"
    ctx = {'overlap':overlap}

    return JsonResponse(ctx)


def student_list(request):
    page = int(request.GET.get('page', 1))
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    students_count = Student.objects.all().count()
    students = Student.objects.all()[offset:limit]
    page_total = ceil(students_count/page_size)
    if page_total == 0:
                page_total += 1
                
    ctx = {
        'page':page,
        'page_total':page_total,
        'page_range':range(1, page_total),
        'students':students,
    }
    return render(request, 'students/student_list.html', ctx)

# 학생 정보 수정 페이지
def student_detail(request, pk):
    students = Student.objects.all()
    ctx = {
        'students':students
    }
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.student_id = request.POST.get('student_id')
            student.name = request.POST.get('name')
            student.phone_number = request.POST.get('phone_number')
            student.email = request.POST.get('email')
            student.status = request.POST.get('status')
            student.save()
            return redirect('students:student_list')
    
    else:
        form = StudentForm(instance=student)
    return render(request,'students/student_detail.html',{'form':form})

# 학생 정보 삭제 페이지
def student_remove(request, pk):
    students = Student.objects.all()
    ctx = {
        'students':students
    }
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('students:student_list')
    
    else:
        form = StudentForm(instance=student)
    return render(request,'students/student_remove.html',{'form':form})

#학생 목록에서 조회하는 뷰
def list_search(request):
    search_key = request.GET.get('search_key') # 검색어 가져오기
    search_list = Student.objects.all()

    if search_key: # 만약 검색어가 존재하면
        search_list = search_list.filter(Q(name__contains=search_key)|Q(student_id__contains=search_key)|Q(phone_number__contains=search_key)|Q(email__contains=search_key)) 

        ctx = {
                'search_list': search_list
        }
        
        return render(request, 'students/lookup_student_list.html', ctx)
