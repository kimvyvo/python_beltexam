from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9copy.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_login(self, postData):
        errors = {}
        if len(postData['lemail']) < 1 or not EMAIL_REGEX.match(postData['lemail']):
            errors['email'] = 'Invalid email.'
        elif len(User.objects.filter(email=postData['lemail'])) == 0:
            errors['email'] = 'Email is not registered.'
        if len(postData['password']) < 1:
            errors['password'] = 'Password cannot be blank.'
        elif len(User.objects.filter(email=postData['lemail'])) != 0:
            user = User.objects.get(email=postData['lemail'])
            if bcrypt.checkpw(postData['password'].encode(), user.pw_hash.encode()) == False:
                errors['login'] = 'Email and password do not match.'
        return errors
    
    def validate_register(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters.'
        elif str.isalpha(postData['first_name']) == False:
            errors['first_name'] = 'Name can only contain letters.'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters.'
        elif str.isalpha(postData['first_name']) == False:
            errors['last_name'] = 'Name can only contain letters.'
        if len(postData['remail']) < 1 or not EMAIL_REGEX.match(postData['remail']):
            errors['email'] = 'Invalid email.'
        elif len(User.objects.filter(email=postData['remail'])) != 0:
            errors['email'] = 'Email already taken.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters.'
        elif postData['confirm_password'] != postData['password']:
            errors['confirm_password'] = 'Passwords do not match.'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()