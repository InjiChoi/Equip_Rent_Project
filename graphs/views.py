from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/users/')
def graph_main(request):
    return render(request, 'graphs/graph.html')