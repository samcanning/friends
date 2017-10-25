# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms

import re
import bcrypt
import datetime

class UserMgr(models.Manager):
    def regvalidator(self, postData): #validates registration attempts
        errors = {}
        emailRegex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" #email format
        nameRegex = r"(^[a-zA-Z]+(([' -][a-zA-Z ])?[a-zA-Z]*)*$)" #must begin with a letter, allows for spaces and hyphenated names, but must also end with a letter
        aliasRegex = r"(^[a-zA-Z0-9_-]+$)" #alias may only be letters, numbers, underscores, and dashes
        pwRegex = r"(^[a-zA-Z0-9_.!?-]+$)" #valid password characters (alphanumeric characters or _.!?-)

        #name
        if not re.match(nameRegex, postData['name']):
            errors['name'] = "Must enter a valid name."
        else:
            if len(postData['name']) < 5:
                errors['name'] = "Name must be at least 5 characters."
            elif len(postData['name']) > 255:
                errors['name'] = "Name cannot be longer than 255 characters."
        #alias
        if not re.match(aliasRegex, postData['alias']):
            errors['alias'] = "Must enter a valid alias."
        elif len(postData['alias']) < 3:
            errors['alias'] = "Alias must be at least 3 characters."
        elif len(postData['alias']) > 40:
            errors['alias'] = "Alias cannot be longer than 40 characters."
        elif User.objects.filter(alias=postData['alias']).exists():
            errors['alias'] = "This alias is already in use."
        
        #dob
        if postData['dob'] == '':
            errors['dob'] = "Must enter a valid date of birth."
        if str(postData['dob']) > str(datetime.date.today()):
            errors['dob'] = "You haven't been born yet!"
        latestAllowed = datetime.date(2003, 10, 25) #definitely a better way to do this, this way it would have to be recoded every single day
        if str(postData['dob']) > str(latestAllowed):
            errors['dob'] = "Must be at least 14 years old."
        #email
        if not re.match(emailRegex, postData['email']):
            errors['email'] = "Must be a valid email address."
        elif User.objects.filter(email=postData['email']).exists():
            errors['email'] = "This email address is already in use."
        #password
        if str.lower(str(postData['password'])) == 'password':
            errors['password'] = "Password cannot be 'password'."
        elif not re.match(pwRegex, postData['password']):
            errors['password'] = "Not a valid password."
        else:
            if len(postData['password']) < 8:
                errors['password'] = "Password must be at least 8 characters."
            elif postData['password'] != postData['confirmpw']:
                errors['password'] = "Passwords must match."
        return errors

    def loginvalidator(self, postData): #validates login attempts
        errors = {}
        try:
            this = User.objects.get(email=postData['email'])
        except:
            errors['email'] = "No user found with this email address."
        
        if 'email' not in errors:
            pw_attempt = str(postData['password'])
            pw_to_check = str(this.password)
            if not bcrypt.checkpw(pw_attempt, pw_to_check):
                errors['password'] = "Incorrect password."
        return errors
        
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    dob = models.DateField()
    friends = models.ManyToManyField("self", related_name="friends")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserMgr()