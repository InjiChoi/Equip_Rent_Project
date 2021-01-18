from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from equipments.models import Equipment
from django.db.models import Q

@login_required(login_url='/users/')
def graph_main(request):
    laptops = Equipment.objects.filter(equip_type='laptop').count()
    l_rent = Equipment.objects.filter((Q(rent_status='impossible')|Q(rent_status='pending')), equip_type='laptop').count()

    tablets = Equipment.objects.filter(equip_type='tablet').count()
    t_rent = Equipment.objects.filter((Q(rent_status='impossible')|Q(rent_status='pending')), equip_type='tablet').count()

    sensors = Equipment.objects.filter(equip_type='sensor').count()
    s_rent = Equipment.objects.filter((Q(rent_status='impossible')|Q(rent_status='pending')), equip_type='sensor').count()

    equip = [laptops, tablets, sensors,]
    rent = [l_rent, t_rent, s_rent,]

    labels = ['노트북', '태블릿', '센서']
    ctx = {
        'equip':equip,
        'rent':rent,
        'labels':labels,
    }
    return render(request, 'graphs/graph.html', ctx)


@login_required(login_url='/users/')
def graph_laptop(request):
    laptops = Equipment.objects.filter(equip_type='laptop')
    sum = laptops.count()
    l_possible = Equipment.objects.filter(equip_type='laptop', rent_status='possible').count()
    l_impossible = Equipment.objects.filter(equip_type='laptop', rent_status='impossible').count()
    l_pending = Equipment.objects.filter(equip_type='laptop', rent_status='pending').count()

    data = [l_possible, l_impossible, l_pending]
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

    data = [t_possible, t_impossible, t_pending]
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

    data = [s_possible, s_impossible, s_pending]
    labels = ['대여 가능', '대여중', '반납 보류']
    ctx = {
        'data':data,
        'labels':labels,
    }
    return render(request, 'graphs/graph_sensor.html', ctx)