from sre_parse import CATEGORIES
from unicodedata import category
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=10, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Apartment(models.Model):

    DISTRICT_CHOICES = [
        ('Thanh Khê', 'Thanh Khê'),
        ('Hải Châu', 'Hải Châu'),
        ('Liên Chiểu', 'Liên Chiểu'),
        ('Sơn Trà', 'Sơn Trà'),
        ('Ngũ Hành Sơn', 'Ngũ Hành Sơn'),
        ('Cẩm Lệ', 'Cẩm Lệ'),
        ('Hòa Vang', 'Hòa Vang'),
        ('Hoàng Sa', 'Hoàng Sa')
    ]

    CATEGORIES_CHOICES = [
        ('rent', 'rent'),
        ('sale', 'sale')
    ]
    
    category = models.CharField(max_length=5, choices=CATEGORIES_CHOICES, blank=False)
    address = models.CharField(max_length=50, unique=True, blank=False)
    district = models.CharField(max_length=20, choices=DISTRICT_CHOICES, blank=False)
    arena = models.FloatField()
    price = models.IntegerField(blank=False)
    description = models.TextField(max_length=200)
    seller = models.ForeignKey('User', related_name='apartment', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(
        auto_now_add=True)
    issold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address}, {self.arena}m2"



class Transaction(models.Model):
    buyer = models.ForeignKey(
        'User', related_name='transaction', on_delete=models.CASCADE)
    apartment = models.OneToOneField(
        'Apartment', related_name='sold', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.buyer} {self.apartment}"
