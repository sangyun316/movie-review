from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError
from django.db.models import Count
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
# Create your models here.


class UserManager(models.Manager):

    def validateReg(self, request):
        errors = self.validateInputs(request)

        try:
            if len(errors) > 0:
                return (False, errors)

            hashed_pw = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt())

            user = self.create(first_name=request.POST['first_name'], last_name=request.POST[
                               'last_name'], email=request.POST['email'], hashed_pw=hashed_pw)

        except IntegrityError:
            # catch *all* exceptions
                # 1 import sys
                # 2 try:
                # 3   conditions
                # 4 except:
                # 5   e = sys.exc_info()[0]
                # 6   print( e )
            return (False, ["Email already in use"])

        return (True, user)

    def validateLogin(self, request):
        try:
            user = User.objects.get(email=request.POST['email'])
            password = request.POST['password'].encode()
            if bcrypt.hashpw(password, user.hashed_pw.encode()) == user.hashed_pw:
                return (True, user)
            else:
                return (False, ["Email/password does not match"])

        except ObjectDoesNotExist:
            return (False, ["Email is not registered with this site"])

    def validateInputs(self, request):
        errors = []
        if len(request.POST['first_name']) < 2:
            errors.append("First Name must be longer than 2 characters.")
        if len(request.POST['last_name']) < 2:
            errors.append("Last Name must be longer than 2 characters.")
        if len(request.POST['email']) == 0:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(request.POST['email']):
            errors.append("Email is not valid!")

        if len(request.POST['password']) < 8 or request.POST['password'] != request.POST['confirm_pw']:
            errors.append("Passwords must match and be at least 8 characters.")

        return errors

    def fetch_user_info(self, id):
        return self.filter(id=id).annotate(total_reviews=Count('review'))[0]


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    hashed_pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
