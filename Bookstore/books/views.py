from django.shortcuts import render
from django.http import HttpResponse
from cuser.models import User

def homeview(request):
    return render(request, 'home.html')