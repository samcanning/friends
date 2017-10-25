# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    if 'logged' not in request.session:
        request.session['logged'] = False
    return render(request, 'login/index.html')

def register(request):

    #---------- Validate Registration Attempt ----------
    errors = User.objects.regvalidator(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags='reg')
        return redirect('/')

    #---------- Create User If Valid ----------
    else:
        temp = str(request.POST['password'])
        hashed_pw = bcrypt.hashpw(temp, bcrypt.gensalt()) #encrypt password before storing in database!!!
        User.objects.create(name=request.POST['name'], alias=request.POST['alias'], dob=request.POST['dob'], email=request.POST['email'], password=hashed_pw)
        request.session['logged'] = True
        request.session['user_id'] = User.objects.get(email=request.POST['email']).id
        return redirect('/friends')

def login(request):

    #---------- Validate Login Attempt ----------
    errors = User.objects.loginvalidator(request.POST) #checks to ensure entered email is in use, and password matches
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags='login')
        return redirect('/')
    #if no errors found, sends the User through
    context = {
        'user': User.objects.get(email=request.POST['email']),
    }
    request.session['logged'] = True
    request.session['user_id'] = User.objects.get(email=request.POST['email']).id
    return redirect('/friends')

def main(request):
    if request.session['logged'] == False:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'others': User.objects.exclude(id=request.session['user_id'])
    }
    return render(request, 'friends/index.html', context)

def logout(request):
    request.session['logged'] = False
    request.session['user_id'] = None
    return redirect('/')