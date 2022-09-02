from django.contrib.auth.models import AbstractUser
from django.db import models
from djongo import models as testing

from django.db import models
from django.contrib.auth.models import User



class Permission(models.Model):
    id = testing.ObjectIdField()
    name = testing.CharField(max_length=200)

class Role(models.Model):
    id = testing.ObjectIdField()
    name = testing.CharField(max_length=200)
    permissions = testing.ArrayField(model_container = Permission)

class User(AbstractUser):
    first_name = testing.CharField(max_length=200)
    last_name = testing.CharField(max_length=200)
    email = testing.CharField(max_length=200,unique=True)
    password=testing.CharField(max_length=200)
    role = testing.ForeignKey(Role,on_delete=models.SET_NULL,null=True)
    username = None

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=[]
   

