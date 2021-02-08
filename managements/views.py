from django.shortcuts import render, redirect, get_object_or_404
from .models import RentManage, ReturnHistory, Equip_Picture, PendingHistory, PendingEquipPicture
from students.models import Student
from equipments.models import Equipment
from managements.forms import RentForm, ReturnForm
from students.models import Student
from django.utils import timezone
from django.db import IntegrityError
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
import xlwt
from datetime import datetime

@login_required(login_url='/users/')
def main_page(request):
    return render(request, 'managements/main.html',{})


# 대여 페이지
@login_required(login_url='/users/')
def rent(request):
        if request.method == 'POST':
                rent_student_id = request.POST.get('student_id')
                rent_equipment_id = request.POST.get('equip_id')
                tag_attach = request.POST.get('tag_attach')
                equip_work = request.POST.get('equip_work')
                manager = request.POST.get('manager')
                accessories = request.POST.get('accessories')
                rent_pics = request.FILES.getlist('file')

                rent_student = get_object_or_404(Student, student_id=rent_student_id)
                rent_equip = get_object_or_404(Equipment, equip_id=rent_equipment_id)

                rent_form = RentForm(request.POST, request.FILES)

                if rent_form.is_valid()  :
                        rent_info = rent_form.save(commit=False)
                        rent_info.student = rent_student
                        rent_info.equip = rent_equip
                        rent_info.tag_attach = tag_attach
                        rent_info.equip_work = equip_work
                        if rent_info.accessories is not None:
                                rent_info.accessories = accessories
                        rent_info.manager = manager
                        rent_info.rent_date = timezone.now()
                        rent_equip.rent_status = 'impossible'
                        rent_equip.save()
                        rent_info.save()

                        for item in rent_pics:
                                images = Equip_Picture.objects.create(rent=rent_info, equip_pic=item)
                                images.save()
                       
                        current_site = get_current_site(request) 
                        html_message = render_to_string('managements/user_activate_email.html', {
                                'rent_info': rent_info,
                                'domain': current_site.domain,
                        })
                        mail_title = "숙명여자대학교 IT공학과 기자재 대여 서약서"
                        email = EmailMultiAlternatives(subject = mail_title, body=html_message, to=[rent_student.email])
                        email.content_subtype = 'html'
                        email.send()
                return redirect('managements:rent_list')
        else:
                rent_form = RentForm()
                ctx = {
                        'rent_form':rent_form,
                }
                return render(request, 'managements/rent.html', ctx)

def activate(request, pk):
        rentmanage = RentManage.objects.get(pk=pk)
        rentmanage.active = True
        rentmanage.save()
        return redirect("managements:email_success")

def email_success(request):
        return render(request, 'managements/email_success.html')

# 대여 중복 검사
@login_required(login_url='/users/')
def rent_overlap_check(request):
        equip_id = request.GET.get('equip_id')
        student_id = request.GET.get('student_id')
        overlap = "init"
        try: # 기자재 존재 여부 확인
                equipment = Equipment.objects.get(equip_id=equip_id)
        except:
                equipment = None

        try: # 학생 존재 여부 확인
                student = Student.objects.get(student_id=student_id)
        except:
                student = None    

        try: # 대여 리스트 중복 여부 확인
                rent_equip = Equipment.objects.get(equip_id=equip_id)
                r_equip = RentManage.objects.get(equip=rent_equip)
        except:
                r_equip = None

        if equipment is None: # 기자재 존재하지 않을 시
                e_exist = "fail"
                overlap = 'none'
        elif equipment is not None: # 기자재 존재 시
                e_exist = "pass"
                if r_equip is None and student is not None: # 대여 가능한 기자재
                        overlap = "pass"
                elif r_equip is not None: # 이미 대여중인 기자재
                        overlap = "e_fail"
                elif r_equip is None and student is None:
                        overlap = "s_fail"

        if student is None: # 학생 존재하지 않을 시
                s_exist = "fail"
        elif student is not None: # 학생 존재 시
                s_exist = "pass"
        
        ctx = {
                'overlap': overlap, 
                'e_exist': e_exist,
                's_exist':s_exist,
        }

        return JsonResponse(ctx)

# 반납 존재 여부 검사
@login_required(login_url='/users/')
def return_exist_check(request):
        equip_id = request.GET.get('equip_id')
        student_id = request.GET.get('student_id')

        try: # 기자재 존재 여부 확인
                equipment = Equipment.objects.get(equip_id=equip_id)
        except:
                equipment = None

        try: # 학생 존재 여부 확인
                student = Student.objects.get(student_id=student_id)
        except:
                student = None    

        try: # 대여 리스트 중복 여부 확인
                rent_equip = Equipment.objects.get(equip_id=equip_id)
                rent_student = Student.objects.get(student_id=student_id)
                rent = RentManage.objects.get(equip=rent_equip, student=rent_student)
        except:
                rent = None

        if equipment is None: # 기자재 존재하지 않을 시
                e_exist = "fail"
        elif equipment is not None:
                e_exist = "pass"

        if student is None: # 학생 존재하지 않을 시
                s_exist = "fail"
        elif student is not None: # 학생 존재 시
                s_exist = "pass"

        if student is not None and equipment is not None:
                if rent is None:
                        r_exist = "fail"
                elif rent is not None:
                        r_exist = "pass" 
        else :
                r_exist = "none"

        ctx = {
                'r_exist': r_exist, 
                'e_exist': e_exist,
                's_exist':s_exist,
        }

        return JsonResponse(ctx)

#대여 현황 
@login_required(login_url='/users/')
def rent_list(request):
        rent = RentManage.objects.all().order_by('-id')
        paginator = Paginator(rent,10)
        page = request.GET.get('page')
        rents = paginator.get_page(page)
        ctx = {
                'rents':rents,
        }
        return render(request, 'managements/rent_list.html', ctx)


# 대여 리스트 엑셀 export
@login_required(login_url='/users/')
def rent_excel_download(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="rent_list.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('RentManage_rent')
    row_num = 0 # sheet header
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['학번', '이름', '학적상태', '물품번호', '물품종류', '물품태그', '기기작동', '악세서리', '대여일', '검사자', '서약서']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()
    rows = RentManage.objects.all().values_list('student__student_id', 'student__name', 'student__status', 'equip__equip_id', 'equip__equip_type', 'tag_attach', 'equip_work', 'accessories', 'rent_date', 'manager', 'active')
    
    rows = [[rent_date.strftime("%Y-%m-%d") if isinstance(rent_date, datetime) else rent_date for rent_date in row] for row in rows ]
    for row in rows :
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    
    wb.save(response)
    return response        

# ----------------------------------------------------------------------- #

# 반납 폼 페이지
@login_required(login_url='/users/')
def return_(request):
        if request.method =='POST':
                equip_id = request.POST.get('equip_id')
                student_id = request.POST.get('student_id')
                manager = request.POST.get('manager')

                try :   
                        student = get_object_or_404(Student, student_id=student_id)
                        equip = get_object_or_404(Equipment,equip_id=equip_id)
                        rent = get_object_or_404(RentManage, equip=equip.pk)
                        rent_images = Equip_Picture.objects.all().filter(rent=rent.pk)

                        ctx = {
                                'student':student,
                                'equip':equip,
                                'rent':rent,
                                'rent_images':rent_images,
                                'manager' : manager
                        }

                        return render(request,'managements/return_info.html',ctx)
                except :
                        return_form = ReturnForm()
                        ctx = {
                                'return_form':return_form
                        }

                        return render(request, 'managements/return.html', ctx)

        else : 
                return_form = ReturnForm()
                ctx = {
                        'return_form':return_form
                }

                return render(request, 'managements/return.html', ctx)


# 반납 처리 view
@login_required(login_url='/users/')       
def return_result(request, pk, manager):
        rent_equip = Equipment.objects.get(pk=pk)
        rent_equip.rent_status = 'possible'
        rent_equip.save()
        rent = RentManage.objects.get(equip = rent_equip)
        rent_student = Student.objects.get(student_id=rent.student.student_id)
        return_instance = ReturnHistory.objects.create(student=rent_student, equip=rent_equip, return_date=timezone.now() ,manager=manager)
        rent.delete()
        try: 
                pending = PendingHistory.objects.get(equip = rent_equip)
                pending.delete()
        except:
                pending = None
        return redirect('managements:return_list')

# 보류 => 반납 처리 view
def pending_to_return(request, pk):
        print(1)
        if request.method == 'POST':
                print(2)
                manager = request.POST.get('manager')
                print(manager)
                rent_equip = Equipment.objects.get(pk=pk)
                rent_equip.rent_status = 'possible'
                rent_equip.save()
                rent = RentManage.objects.get(equip = rent_equip)
                rent_student = Student.objects.get(student_id=rent.student.student_id)
                return_instance = ReturnHistory.objects.create(student=rent_student, equip=rent_equip, return_date=timezone.now() ,manager=manager)
                rent.delete()
                pending = PendingHistory.objects.get(equip = rent_equip)
                pending.delete()
        return redirect('managements:return_list')

# 보류 폼 작성 view
@login_required(login_url='/users/')
def pending(request, pk):
        rent_equip = Equipment.objects.get(pk=pk)
        rent = RentManage.objects.get(equip = rent_equip)
        ctx = {
                'rent_equip':rent_equip,
                'rent':rent,
        }
        if rent_equip.rent_status == 'pending':
                pending = PendingHistory.objects.get(equip=rent_equip)
                return redirect('managements:pending_detail_page', pending.pk)
        return render(request, 'managements/pending.html', ctx)

# 보류 처리 view
@login_required(login_url='/users/')
def pending_result(request, pk):
        rent_equip = Equipment.objects.get(pk=pk)
        rent_equip.rent_status = 'pending'
        rent_equip.save()
        rent = RentManage.objects.get(equip = rent_equip)
        rent_student = Student.objects.get(pk=rent.student.pk)
        if request.method == 'POST':
                reason = request.POST.get('reason')
                pending = PendingHistory.objects.create(student=rent_student, equip=rent_equip, reason=reason)
                rent_pics = request.FILES.getlist('file')
                for item in rent_pics:
                        images = PendingEquipPicture.objects.create(pending=pending, pending_equip_pic=item)
                        images.save()
                return redirect('managements:pending_list')

        else:
                return redirect('managements:pending', pk)
                

# 반납 목록 페이지
@login_required(login_url='/users/')
def return_list(request):
        return_list = ReturnHistory.objects.all().order_by('-id')
        paginator = Paginator(return_list, 10)
        page = request.GET.get('page')
        returns = paginator.get_page(page)
        ctx = {
                'returns':returns,
        }
        return render(request, 'managements/return_list.html', ctx)

# 반납 리스트 엑셀 export
@login_required(login_url='/users/')
def return_excel_download(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="return_list.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ReturnHistory_Return')
    row_num = 0 # sheet header
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['학번', '이름', '연락처', '물품번호', '물품종류', '검사자', '반납일']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()
    rows = ReturnHistory.objects.all().values_list('student__student_id', 'student__name', 'student__phone_number', 'equip__equip_id', 'equip__equip_type', 'manager', 'return_date')
    
    rows = [[return_date.strftime("%Y-%m-%d") if isinstance(return_date, datetime) else return_date for return_date in row] for row in rows ]
    for row in rows :
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    
    wb.save(response)
    return response  

#대여시 학생 조회
@login_required(login_url='/users/')
def lookup_student(request):
        input_student = request.GET.get('input_student')
        try : 
                student = Student.objects.get(student_id=input_student)
                name = student.name
                phone_number = student.phone_number
                email = student.email

                ctx = {
                        'name':name,
                        'phone_number':phone_number,
                        'email':email
                }
                return render(request,'managements/lookup.html',ctx)
        
        except :
                
                return render(request, 'managements/lookup_fail.html')

#반납 리스트에서 검색하는 뷰
@login_required(login_url='/users/')
def search_return_list(request):
    search_input = request.GET.get('search_input')
    selected_equip_type = request.GET.get('search_select')
    
    if selected_equip_type == "":
        selected_equip_type = False

    if search_input and selected_equip_type:
        search_list = ReturnHistory.objects.all().filter(((Q(student__name__contains=search_input)|Q(student__student_id__contains=search_input)|Q(student__phone_number__contains=search_input))|Q(equip__equip_id__contains=search_input)), equip__equip_type__contains=selected_equip_type).order_by('-id')

    elif search_input:
        search_list = ReturnHistory.objects.all().filter(Q(equip__equip_id__contains=search_input)|Q(student__name__contains=search_input)|Q(student__student_id__contains=search_input)|Q(student__phone_number__contains=search_input)).order_by('-id')

    elif selected_equip_type:
        search_list = ReturnHistory.objects.all().filter(equip__equip_type__contains=selected_equip_type).order_by('-id')

    else:
        search_list = ReturnHistory.objects.all().order_by('-id')

    paginator = Paginator(search_list, 10)
    page = request.GET.get('page')
    returns = paginator.get_page(page)

    ctx = {
        'returns':returns,
    }

    return render(request, 'managements/return_list_search.html', ctx)   


#대여 리스트에서 검색하는 뷰
@login_required(login_url='/users/')
def search_rent_list(request):
        search_input = request.GET.get('search_input')
        selected_equip_type = request.GET.get('search_select')
        
        if selected_equip_type == "":
                selected_equip_type = False

        
        if search_input and selected_equip_type:
                search_list = RentManage.objects.all().filter(((Q(student__name__contains=search_input)|Q(student__student_id__contains=search_input))|Q(equip__equip_id__contains=search_input)), equip__equip_type__contains=selected_equip_type)

        elif search_input:
                search_list = RentManage.objects.all().filter(Q(equip__equip_id__contains=search_input)|Q(student__name__contains=search_input)|Q(student__student_id__contains=search_input))

        elif selected_equip_type:
                search_list = RentManage.objects.all().filter(equip__equip_type__contains=selected_equip_type)

        else:
                search_list = RentManage.objects.all()

        search_list = search_list.order_by('-id')
        paginator = Paginator(search_list,10)
        page = request.GET.get('page')
        rents = paginator.get_page(page)
        ctx = {
                'rents':rents
        }

        return render(request, 'managements/rent_list_search_1.html', ctx)   

#대여 리스트에서 서약서 여부를 검색하는 뷰
@login_required(login_url='/users/')
def search_rent_pledge(request):
        search_pledge = request.GET.get('search_pledge')
        
        if search_pledge =="":
                search_pledge = None
        
        if search_pledge is not None:
                search_list = RentManage.objects.all().filter(active=search_pledge).order_by('-id')
        else:
                search_list = RentManage.objects.all().order_by('-id')
        
        paginator = Paginator(search_list,10)
        page = request.GET.get('page')
        rents = paginator.get_page(page)
        ctx = {
                "rents":rents
        }

        return render(request,'managements/rent_list_search_2.html',ctx)

#대여 리스트에서 대여별 상세페이지 관련 뷰
@login_required(login_url='/users')
def rent_detail_page(request,pk):
        rent = get_object_or_404(RentManage,pk=pk)
        rent_images = Equip_Picture.objects.all().filter(rent=rent.pk)
        ctx={
                'rent':rent,
                'rent_images':rent_images
        }
        return render(request,'managements/rent_detail.html',ctx)

#대여 상세페이지에서 서약서 메일 재발송 관련 뷰
@login_required(login_url='/users')
def resend_pledge(request,pk):
        rent = get_object_or_404(RentManage,pk=pk)
        current_site = get_current_site(request) 
        html_message = render_to_string('managements/user_activate_email.html', {
                'rent_info': rent,
                'domain': current_site.domain,
        })
        mail_title = "숙명여자대학교 IT공학과 기자재 대여 서약서"
        email = EmailMultiAlternatives(subject = mail_title, body=html_message, to=[rent.student.email])
        email.content_subtype = 'html'
        email.send()
        return redirect('managements:rent_detail_page',pk)

# 보류 목록 페이지
@login_required(login_url='/users/')
def pending_list(request):
        pending = PendingHistory.objects.all().order_by('-id')
        paginator = Paginator(pending,10)
        page = request.GET.get('page')
        pendings = paginator.get_page(page)

        ctx = {
                'pendings':pendings
        }
        return render(request, 'managements/pending_list.html', ctx)

# 보류 리스트 엑셀 export
@login_required(login_url='/users/')
def pending_excel_download(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="pending_list.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('PendingHistory_Pending')
    row_num = 0 # sheet header
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['학번', '이름', '연락처', '물품번호', '물품종류', '보류일', '보류사유']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()
    rows = PendingHistory.objects.all().values_list('student__student_id', 'student__name', 'student__phone_number', 'equip__equip_id', 'equip__equip_type', 'pending_date', 'reason')
    
    rows = [[pending_date.strftime("%Y-%m-%d") if isinstance(pending_date, datetime) else pending_date for pending_date in row] for row in rows ]
    for row in rows :
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    
    wb.save(response)
    return response  


#보류 리스트에서 보류 별 상세 페이지 뷰
@login_required(login_url='/users')
def pending_detail(request, pk):
        pending = PendingHistory.objects.get(pk=pk)
        pending_images = PendingEquipPicture.objects.all().filter(pending=pending.pk)
        rent_images = Equip_Picture.objects.all().filter(rent__equip=pending.equip)
        ctx = {
                'pending':pending,
                'pending_images':pending_images,
                'rent_images':rent_images,
        }
        return render(request, 'managements/pending_detail.html', ctx)


# 보류 중복 검사
@login_required(login_url='/users/')
def pending_overlap_check(request):
        equip_id = request.GET.get('equip_id')
        equip = Equipment.objects.get(equip_id=equip_id)
        try:
                pending = PendingHistory.objects.get(equip=equip)
        except:
                pending = None

        if pending is not None:
                overlap='fail'
        else:
                overlap='pass'

        ctx = {
                'overlap':overlap,
        }
        return JsonResponse(ctx)

# 보류 목록 검색
@login_required(login_url='/users/')
def search_pending_list(request):
        search_input = request.GET.get('search_input')
        selected_equip_type = request.GET.get('search_select')
        if selected_equip_type == "":
                selected_equip_type = False
        
        if search_input and selected_equip_type:
                search_list = PendingHistory.objects.all().filter(((Q(student__name__contains=search_input)|Q(student__student_id__contains=search_input)|Q(student__phone_number__contains=search_input))|Q(equip__equip_id__contains=search_input)), equip__equip_type__contains=selected_equip_type)

        elif search_input:
                search_list = PendingHistory.objects.all().filter(Q(equip__equip_id__contains=search_input)|Q(student__name__contains=search_input)|Q(student__student_id__contains=search_input)|Q(student__phone_number__contains=search_input))

        elif selected_equip_type:
                search_list = PendingHistory.objects.all().filter(equip__equip_type__contains=selected_equip_type)

        else:
                search_list = PendingHistory.objects.all()

        search_list = search_list.order_by('-id')
        paginator = Paginator(search_list,10)
        page = request.GET.get('page')
        pendings = paginator.get_page(page)
        ctx = {
                'pendings':pendings
        }

        return render(request, 'managements/pending_list_search.html', ctx)   