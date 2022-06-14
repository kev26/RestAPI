from django.shortcuts import render
from psycopg2 import Timestamp
from requests import request
from rest_framework.response import Response
from rest_framework import viewsets, permissions
# from timTro.permissions import IsOwnerOrReadOnly
from rest_framework.authtoken.models import Token

from .models import User, Apartment, Transaction
from .serializers import UserSerializer, ApartmentSerializer, TransactionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ApartmentViewset(viewsets.ModelViewSet):
    queryset = Apartment.objects.filter(issold=False).order_by('-timestamp')
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # fill current username when create new apartment
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class SoldViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Apartment.objects.filter(issold=True).order_by('-timestamp')
    serializer_class = ApartmentSerializer


class TransactionViewset(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-timestamp')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        transaction = serializer.save(buyer=self.request.user)
        transaction.apartment.issold = True
        transaction.apartment.save()
