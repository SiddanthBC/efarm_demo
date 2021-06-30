import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from random import randint
from . import database
from .models import *
import json
import socket

# Create your views here.

def index(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def health(request):
    """Takes an request as a parameter and gives the count of pageview objects as reponse"""
    return HttpResponse(PageView.objects.count())

def reg(request):
    if request.method == 'POST':
        username = request.POST['Username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
    
        user =  creds(name=username, password=password1, email=email)
        user.save()
        return render(request, 'login.html')
    else:
        return render(request, 'reg.html',{'creds1':creds})

def login(request):
    return render(request, 'login.html')

def iot(request):
    # temp = randint(20,35)
    # humidity = randint(25,100)
    # soil_moisture = randint(25,100)

    # sdata = {
    #     'temp':temp,
    #     'humidity':humidity,
    #     'soil_moisture':soil_moisture,
    
    # }
    # print(sdata)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.162.73', 65432))
        data = s.recv(1024)
    sdata = json.loads(data)
    print('<-'*10,'Data Received','->'*10,'\n')
    print('Humidity: ',sdata['humidity'],'\n')
    print('Temparature: ',sdata['temp'],'\n')    
    print('Moisture: ',sdata['moisture'],'\n')
    return render(request, 'iot.html', sdata)


