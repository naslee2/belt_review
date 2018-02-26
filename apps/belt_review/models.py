from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX=re.compile(r'^[a-zA-Z0-9]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z\s]+$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData['name']) < 1:
            errors['name'] = "Name should be more than 1 character!"
        elif not NAME_REGEX.match(postData['name']):
            errors['name'] = "Name should not have any numbers!"

        if len(postData['alias']) < 1:
            errors['alias'] = "Alias should be more than 1 character!"

        if EMAIL_REGEX.match(postData['email']):
            dup = User.objects.filter(email=postData['email'])
            if len(dup) > 0:
                errors['email'] = "Email is already registered!"
        else:
            errors['email'] = "Must put in a Valid Email!"

        if len(postData['password'])< 7:
            errors['password'] = "Must put in a Valid Password!"
        elif not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Must put in a Valid Password!"
            
        if len(postData['confirm_pw'])< 7:
            errors['confirm_pw'] = "Must put in a Valid Password!"
        elif not PASSWORD_REGEX.match(postData['confirm_pw']):
            errors['confirm_pw'] = "Must put in a Valid Password!"
        elif not postData['password'] == postData['confirm_pw']:
            errors['confirm_pw'] = "Passwords must be the same!"
        if len(errors) < 1:
            reg_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            reg_user = User.objects.create(name=postData['name'], alias=postData['alias'], email=postData['email'], password=reg_hash)
            errors['valid_user'] = reg_user
        return errors

    def validator2(self, postData):
        errors2={}
        check = User.objects.filter(email=postData['login_email'])
        if check:
            check2 = check[0].email
            check3 = check[0].password
            if bcrypt.checkpw(postData['login_password'].encode(), check3.encode()):
                errors2['success'] = check[0] 
                return errors2
            else: 
                errors2['login_password'] = "Invalid 0101"
                return errors2
        else:
            errors2['login_password'] = "Invalid 0011"
            return errors2

    def validator3(self,postData):
        errors3={}
        if len(postData['title']) <1:
            errors3['title'] = "Title should be more than 1 character!"
        else:
            if 'new_author' in postData:
                errors3['success']= postData['new_author']
            elif 'list_author' in postData:
                errors3['success']= postData['list_author']
        return errors3
    
    def validator4(self,postData):
        errors4={}
        if len(postData['add_review']) <5:
            errors4['add_review'] = "Review should be more than 5 characters long!"
        else:
            errors4['success']=postData['add_review']
        return errors4

class User(models.Model):
    name=models.CharField(max_length=255)
    alias=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=45)
    objects= UserManager()

class Book(models.Model):
    book_title=models.CharField(max_length=255)
    author=models.CharField(max_length=255)
    uploaded_by=models.ForeignKey(User, related_name="uploader")
    objects= UserManager()

class Review(models.Model):
    review=models.TextField()
    rating=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    users=models.ForeignKey(User, related_name="reviewer")
    books=models.ForeignKey(Book, related_name="review")
    objects= UserManager()