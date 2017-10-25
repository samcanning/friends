# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..login.models import User

def index(request): #displays main page if user is logged in
    if request.session['logged'] == False:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'myfriends': User.objects.get(id=request.session['user_id']).friends.all(),
        'nonfriends': User.objects.exclude(friends__in=[request.session['user_id']]).exclude(id=request.session['user_id']).all(),
    }
    return render(request, 'friends/index.html', context)

def profile(request, friend): #displays user profiles (with information hidden if user is not logged in)
    if request.session['logged'] == True:
        context = {
            'yourfriends': User.objects.get(id=request.session['user_id']).friends.all(),
            'user': User.objects.get(id=request.session['user_id']),
            'friend': User.objects.get(id=friend),
        }
    else:
        context = {
            'friend': User.objects.get(id=friend),
        }
    return render(request, 'friends/profile.html', context)

def unfriend(request, friend): #removes friend from user's friends list
    if request.session['logged'] == False:
        return redirect('/')
    User.objects.get(id=request.session['user_id']).friends.remove(User.objects.get(id=friend))
    return redirect('/friends')

def add(request, friend): #adds friend to user's friends list
    if request.session['logged'] == False:
        return redirect('/')
    User.objects.get(id=request.session['user_id']).friends.add(User.objects.get(id=friend))
    return redirect('/friends')

def addredirect(request, friend): #same as add, but with redirect back to user profile (for adding a user from their profile)
    if request.session['logged'] == False:
        return redirect('/')
    User.objects.get(id=request.session['user_id']).friends.add(User.objects.get(id=friend))
    return redirect('/friends/profile/' + friend)