from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

def index(request):
    if not request.session.keys():
        request.session['first_name'] = ''
        request.session['last_name'] = ''
        request.session['remail'] = ''
        request.session['lemail'] = ''
    return render(request, 'logreg/index.html')

def login(request, methods=['POST']):
    request.session['lemail'] = request.POST['lemail']
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    else: 
        request.session['user_id'] = User.objects.get(email=request.session['lemail']).id
        return redirect('/success')

def register(request, methods=['POST']):
    request.session['first_name'] = request.POST['first_name']
    request.session['last_name'] = request.POST['last_name']
    request.session['remail'] = request.POST['remail']
    errors = User.objects.validate_register(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')
    else:
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['remail'], pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        request.session['user_id'] = User.objects.last().id
        return redirect('/success')

def success(request):
    return render(request, 'logreg/success.html',{'user' : User.objects.get(id=request.session['user_id'])})

def logout(request):
    request.session.clear()
    return redirect('/')