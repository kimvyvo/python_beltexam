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
        return redirect('/quotes')

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
        return redirect('/quotes')

def quotes(request):
    context = {
        'user' : User.objects.get(id=request.session['user_id']),
        'quotes' : Quote.objects.raw('SELECT * FROM logreg_quote ORDER BY created_at DESC;'),
    }
    return render(request, 'logreg/success.html', context)

def display(request, id):
    context = {
        'user' : User.objects.get(id=id),
        'quotes' : Quote.objects.filter(poster_id=id)
    }
    return render(request, 'logreg/display.html', context)

def like(request, methods=['POST']):
    if len(Quote.objects.get(id=request.POST['quote_id']).likes.filter(liker_id=request.session['user_id'])) == 0:
        Like.objects.create(liker=User.objects.get(id=request.session['user_id']), quote=Quote.objects.get(id=request.POST['quote_id']))
    return redirect('/quotes')

def add_quote(request, methods=['POST']):
    request.session['author'] = request.POST['author']
    request.session['quote'] = request.POST['quote']
    errors = Quote.objects.validate_quote(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        Quote.objects.create(author=request.POST['author'], content=request.POST['quote'], poster=User.objects.get(id=request.session['user_id']))
        request.session['author'] = ''
        request.session['quote'] = ''
    return redirect('/quotes')

def delete(request, methods=['POST']):
    Quote.objects.get(id=request.POST['quote_id']).delete()
    return redirect('/quotes')

def edit(request, id):
    return render(request, 'logreg/edit.html', { 'user' : User.objects.get(id=id)})

def update(request, id):
    errors = User.objects.validate_update(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/myaccount/' + id)
    else: 
        u = User.objects.get(id=id)
        u.first_name = request.POST['first_name']
        u.last_name = request.POST['last_name']
        u.email = request.POST['email']
        u.save()
        route = '/edit/' + id
    return redirect('/myaccount/' + id)

def logout(request):
    request.session.clear()
    return redirect('/')