import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from sellHouse.permissions import IsOwnerApartmentOrReadOnly, IsOwnerUserOrReadOnly
from rest_framework.generics import CreateAPIView
from django.contrib.auth.hashers import make_password  # Hash password

from .models import User, Apartment, Transaction
from .serializers import UserSerializer, ApartmentSerializer, TransactionSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class ApartmentViewset(viewsets.ModelViewSet):
    queryset = Apartment.objects.filter(issold=False).order_by('-timestamp')
    serializer_class = ApartmentSerializer
    # Set permission for only user owner apartment can edit it.
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerApartmentOrReadOnly]

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

    # Create a transaction and set issold = True for that Apartment
    def perform_create(self, serializer):
        transaction = serializer.save(buyer=self.request.user)
        transaction.apartment.issold = True
        transaction.apartment.save()