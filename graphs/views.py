from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from equipments.models import Equipment

@login_required(login_url='/users/')
def graph_main(request):
    return render(request, 'graphs/graph.html')


@login_required(login_url='/users/')
def graph_laptop(request):
    laptops = Equipment.objects.filter(equip_type='laptop')
    sum = laptops.count()
    l_possible = Equipment.objects.filter(equip_type='laptop', rent_status='possible').count()
    l_impossible = Equipment.objects.filter(equip_type='laptop', rent_status='impossible').count()
    l_pending = Equipment.objects.filter(equip_type='laptop', rent_status='pending').count()
    if sum !=0:
        poss = round(l_possible/sum * 100)
        imposs = round(l_impossible/sum * 100)
        pend = round(l_pending/sum * 100)
    else:
        poss = 0
        imposs = 0
        pend = 0
    
    data = [poss, imposs, pend]
    labels = ['대여 가능', '대여중', '반납 보류']
    ctx = {
        'data':data,
        'labels':labels,
    }
    return render(request, 'graphs/graph_laptop.html', ctx)


@login_required(login_url='/users/')
def graph_tablet(request):
    tablets = Equipment.objects.filter(equip_type='tablet')
    sum = tablets.count()
    t_possible = Equipment.objects.filter(equip_type='tablet', rent_status='possible').count()
    t_impossible = Equipment.objects.filter(equip_type='tablet', rent_status='impossible').count()
    t_pending = Equipment.objects.filter(equip_type='tablet', rent_status='pending').count()
    if sum !=0:
        poss = round(t_possible/sum * 100)
        imposs = round(t_impossible/sum * 100)
        pend = round(t_pending/sum * 100)
    else:
        poss = 0
        imposs = 0
        pend = 0
    
    data = [poss, imposs, pend]
    labels = ['대여 가능', '대여중', '반납 보류']
    ctx = {
        'data':data,
        'labels':labels,
    }
    return render(request, 'graphs/graph_tablet.html', ctx)

@login_required(login_url='/users/')
def graph_sensor(request):
    sensors = Equipment.objects.filter(equip_type='sensor')
    sum = sensors.count()
    s_possible = Equipment.objects.filter(equip_type='sensor', rent_status='possible').count()
    s_impossible = Equipment.objects.filter(equip_type='sensor', rent_status='impossible').count()
    s_pending = Equipment.objects.filter(equip_type='sensor', rent_status='pending').count()
    if sum !=0:
        poss = round(s_possible/sum * 100)
        imposs = round(s_impossible/sum * 100)
        pend = round(s_pending/sum * 100)
    else:
        poss = 0
        imposs = 0
        pend = 0
    data = [poss, imposs, pend]
    labels = ['대여 가능', '대여중', '반납 보류']
    ctx = {
        'data':data,
        'labels':labels,
    }
    return render(request, 'graphs/graph_sensor.html', ctx)