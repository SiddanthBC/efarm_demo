import os
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from random import randint
from . import database
from welcome.models import creds,PageView
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
    if request.method == "POST":
        username = request.POST['Username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if creds.objects.filter(name=username).exists():
                messages.info(request,"User name Taken")
                return redirect('reg')

            elif creds.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                print('email taken')
                return redirect('reg') 

            else:
                global user
                user =  creds.objects.create(name=username, password=password1, email=email)
                user.save()
                return render(request, 'home.html',{'creds1':user.name})
        else:
            messages.info(request,"Password didn't match")
            return redirect('reg')
    else:
        return render(request, 'reg.html')

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
        host_ip = socket.gethostbyname('proxy60.rt3.io')
        #s.connect(('192.168.29.5', 8080)) #R-pi IP and port connection
        s.connect((host_ip,32741))
        data = s.recv(1024)
    sdata = json.loads(data)
    print('-'*10,'Data Received','-'*10,'\n')
    print('Humidity: ',sdata['humidity'],'\n')
    print('Temparature: ',sdata['temp'],'\n')    
    print('Moisture: ',sdata['soil_moisture'],'\n')

    return render(request, 'iot.html', sdata)

def picam(request):
    return render(request,'picam.html')
