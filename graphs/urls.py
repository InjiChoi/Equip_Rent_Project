from django.urls import path
from . import views

app_name = 'graphs'

urlpatterns = [
    path('', views.graph_main, name='graph_main'),
]
