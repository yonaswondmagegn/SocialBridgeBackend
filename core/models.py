from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager as BaseManager
from django.utils import timezone

class UserManager(BaseManager):

    def _create_user(self,phonenumber,session,password = None,**extra_fields):
        is_superuser = extra_fields.get('is_superuser')
        if not phonenumber:
            raise ValueError('phonenumber is Requred field')
        if not session and not is_superuser:
            raise ValueError('Session is Requred')
        user = self.model(phonenumber = phonenumber,session = session,**extra_fields)
        if  password:
            user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_user(self, phonenumber,session,password =None, **extra_fields):
        extra_fields.setdefault('is_staff',False) 
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(phonenumber,session,password,**extra_fields)
    
    def create_superuser(self, phonenumber,session,password = None,**extra_fields):
        extra_fields.setdefault('is_active',True) 
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(phonenumber,session,password,**extra_fields)


class User(AbstractUser):
    phonenumber = models.CharField(max_length=13,unique=True)
    username = models.CharField(max_length=225,unique=False,null = True,blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = []






