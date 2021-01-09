from django.shortcuts import render, redirect, get_object_or_404
from .models import RentManage, ReturnHistory
from students.models import Student
from equipments.models import Equipment
from managements.forms import RentForm, RentStudentForm, RentEquipmentForm, ReturnForm
from students.models import Student
from django.utils import timezone
from django.db import IntegrityError
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from math import ceil

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


@login_required(login_url='/users/')
def main_page(request):
    return render(request, 'managements/main.html',{})


# 대여 페이지
@login_required(login_url='/users/')
def rent(request):
        if request.method == 'POST':
                rent_student_id = request.POST.get('student_id')
                rent_equipment_id = request.POST.get('equip_id')

                rent_student = get_object_or_404(Student, student_id=rent_student_id)
                rent_equip = get_object_or_404(Equipment, equip_id=rent_equipment_id)

                rent_form = RentForm(request.POST, request.FILES)
                if rent_form.is_valid() :
                        rent_info = rent_form.save(commit=False)
                        rent_info.student = rent_student
                        rent_info.equip = rent_equip
                        rent_info.rent_date = timezone.now()
                        rent_equip.rent_status = True
                        rent_equip.save()
                        rent_info.save()
                        
                        current_site = get_current_site(request) 
                        html_message = render_to_string('managements/user_activate_email.html', {
                                'rent_info': rent_info,
                                'domain': current_site.domain,
                        })
                        mail_title = "이메일 인증을 완료해주세요"
                        email = EmailMultiAlternatives(subject = mail_title, body=html_message, to=[rent_student.email])
                        email.content_subtype = 'html'
                        email.send()
                return redirect('managements:rent_list')
        else:
                rent_form = RentForm()
                rent_student_form = RentStudentForm()
                rent_equipment_form = RentEquipmentForm()
                ctx = {
                        'rent_form':rent_form,
                        'rent_student_form':rent_student_form,
                        'rent_equipment_form':rent_equipment_form,
                }
                return render(request, 'managements/rent.html', ctx)

@login_required(login_url='/users/')
def activate(request, pk):
        rentmanage = RentManage.objects.get(pk=pk)
        rentmanage.active = True
        rentmanage.save()
        return redirect("https://google.com/")


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


@login_required(login_url='/users/')
def rent_list(request):
        page = int(request.GET.get('page', 1))
        page_size = 10
        limit = page_size * page
        offset = limit - page_size
        rents_count = RentManage.objects.all().count()
        rents = RentManage.objects.all()[offset:limit]

        page_total = ceil(rents_count/page_size)
        if page_total == 0:
                page_total += 1
        ctx = {
                'rents':rents,
                'page':page,
                'page_total':page_total,
                'page_range':range(1, page_total),
        }
        return render(request, 'managements/rent_list.html', ctx)

# ----------------------------------------------------------------------- #

# 반납 페이지
@login_required(login_url='/users/')
def return_(request):
        if request.method =='POST':
                equip_id = request.POST.get('equip_id')
                student_id = request.POST.get('student_id')

                try :   
                        student = get_object_or_404(Student, student_id=student_id)
                        equip = get_object_or_404(Equipment,equip_id=equip_id)
                        rent = get_object_or_404(RentManage, equip=equip.pk)

                        ctx = {
                                'student':student,
                                'equip':equip,
                                'rent':rent
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

@login_required(login_url='/users/')       
def return_result(request, pk):
        rent_equip = Equipment.objects.get(pk=pk)
        rent_equip.rent_status = False
        rent_equip.save()
        rent = RentManage.objects.get(equip = rent_equip)
        rent_student = Student.objects.get(student_id=rent.student.student_id)
        return_instance = ReturnHistory.objects.create(student=rent_student, equip=rent_equip, return_date=timezone.now())
        rent.delete()
        return redirect('managements:return_list')

@login_required(login_url='/users/')
def return_list(request):
        page = int(request.GET.get('page', 1))
        page_size = 10
        limit = page_size * page
        offset = limit - page_size
        returns_count = ReturnHistory.objects.all().count()
        returns = ReturnHistory.objects.all()[offset:limit]
        page_total = ceil(returns_count/page_size)
        if page_total == 0:
                page_total += 1
        ctx = {
                'page':page,
                'page_total':page_total,
                'page_range':range(1, page_total),
                'returns':returns,
        }
        return render(request, 'managements/return_list.html', ctx)

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
        search_list = ReturnHistory.objects.all().filter(((Q(student__name__contains=search_input)|Q(student__student_id__contains=search_input)|Q(student__phone_number__contains=search_input))|Q(equip__equip_id__contains=search_input)), equip__equip_type__contains=selected_equip_type)

    elif search_input:
        search_list = ReturnHistory.objects.all().filter(Q(equip__equip_id__contains=search_input)|Q(student__name__contains=search_input)|Q(student__student_id__contains=search_input)|Q(student__phone_number__contains=search_input))

    elif selected_equip_type:
        search_list = ReturnHistory.objects.all().filter(equip__equip_type__contains=selected_equip_type)

    else:
        search_list = ReturnHistory.objects.all()

    ctx = {
        'search_list':search_list
    }

    return render(request, 'managements/lookup_return_list.html', ctx)   


#대여 리스트에서 검색하는 뷰
@login_required(login_url='/users/')
def search_rent_list(request):
    search_input = request.GET.get('search_input')
    selected_equip_type = request.GET.get('search_select')
    
    if selected_equip_type == "":
        selected_equip_type = False

    
    if search_input and selected_equip_type:
        search_list = RentManage.objects.all().filter(((Q(student__name__contains=search_input)|Q(student__student_id__contains=search_input)|Q(student__phone_number__contains=search_input))|Q(equip__equip_id__contains=search_input)), equip__equip_type__contains=selected_equip_type)

    elif search_input:
        search_list = RentManage.objects.all().filter(Q(equip__equip_id__contains=search_input)|Q(student__name__contains=search_input)|Q(student__student_id__contains=search_input)|Q(student__phone_number__contains=search_input))

    elif selected_equip_type:
        search_list = RentManage.objects.all().filter(equip__equip_type__contains=selected_equip_type)

    else:
        search_list = RentManage.objects.all()

    ctx = {
        'search_list':search_list
    }

    return render(request, 'managements/lookup_rent_list.html', ctx)   
                


