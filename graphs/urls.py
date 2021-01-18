from django.urls import path
from . import views

app_name = 'graphs'

urlpatterns = [
    path('', views.graph_main, name='graph_main'),
    path('laptop/', views.graph_laptop, name='graph_laptop'),
    path('tablet/', views.graph_tablet, name='graph_tablet'),
    path('sensor/', views.graph_sensor, name='graph_sensor'),
]
