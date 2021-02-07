from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib import messages
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.validators import FileExtensionValidator
from django.db import IntegrityError
import xlwt

@login_required(login_url='/users/')
def student_register(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_info = student_form.save(commit=False)
            student_info.save()
            return redirect('students:student_list')
        else :
            return redirect('students:student_register')

        return render(request, 'students/student_register.html')
    else:
        student_form = StudentForm()
        return render(request, 'students/student_register.html', {'student_form':student_form})

# 학생 excel 한꺼번에 등록
class UploadFileForm(forms.Form):
    # 파일 확장자는 xlsx, xls로 제한
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])])

@login_required(login_url='/users/')
def student_excel_register(request):
    if request.method == "POST":
        try:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                request.FILES['file'].save_to_database(
                    name_columns_by_row=0, # 첫 번째 행 제목(db upload X)
                    model=Student, # 업로드 대상 모델
                    mapdict=['student_id', 'name', 'phone_number', 'email']) # 업로드 할 데이터 필드
                return redirect('students:student_list')
            else:
                return redirect('students:student_excel_register')
        except IntegrityError: # excel 파일 내에 이미 등록 된 데이터와 중복된 데이터 존재 시
            return redirect('students:student_excel_register')
    else:
        form = UploadFileForm()
    return render(request, 'students/student_excel_register.html', {'form': form})

# 학생 리스트 엑셀 export
@login_required(login_url='/users/')
def student_excel_download(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')
    row_num = 0 # sheet header
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['학번', '이름', '연락처', '이메일', '학적상태']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    
    rows = Student.objects.all().values_list('student_id', 'name', 'phone_number', 'email', 'status')
    for row in rows :
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    
    wb.save(response)
    return response

# 학생 번호 중복 확인
@login_required(login_url='/users/')
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

@login_required(login_url='/users/')
def student_list(request):
    student = Student.objects.all().order_by('-id')
    paginator = Paginator(student, 10)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    ctx = {
        'students':students,
    }
    return render(request, 'students/student_list.html', ctx)

# 학생 정보 수정 페이지
@login_required(login_url='/users/')
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
@login_required(login_url='/users/')
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
@login_required(login_url='/users/')
def list_search(request):
    search_key = request.GET.get('search_key') # 검색어 가져오기
    print(search_key)
    search_list = Student.objects.all()
    if search_key: # 만약 검색어가 존재하면
        search_list = search_list.filter(Q(name__contains=search_key)|Q(student_id__contains=search_key)|Q(phone_number__contains=search_key)|Q(email__contains=search_key)) 
    search_list = search_list.order_by('-id')
    paginator = Paginator(search_list, 10)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    ctx = {
        'students': students,
    }
    return render(request, 'students/student_list_search.html', ctx)
