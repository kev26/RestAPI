from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=10, unique=True, blank=True, null=True)


class Apartment(models.Model):
    seller = models.ForeignKey(
        'User', related_name='apartment', on_delete=models.CASCADE)
    address = models.CharField(max_length=50, unique=True, blank=False)
    arena = models.FloatField()
    price = models.IntegerField(blank=False)
    description = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    issold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address}, {self.arena}m2"


class Transaction(models.Model):
    buyer = models.ForeignKey(
        'User', related_name='transaction', on_delete=models.CASCADE)
    apartment = models.ForeignKey(
        'Apartment', related_name='sold', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.buyer} {self.apartment}"
