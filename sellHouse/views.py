from rest_framework.response import Response
from rest_framework import viewsets, permissions
# from example.sellHouse.filters import ApartmentFilter
from sellHouse.permissions import IsOwnerApartmentOrReadOnly, IsOwnerUserOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ApartmentFilter
from rest_framework.decorators import action

from .models import User, Apartment, Transaction
from .serializers import UserSerializer, ApartmentSerializer, TransactionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Set permission for only user authenticated can see users list and only user itself can edit.
    permission_classes = [
        permissions.IsAuthenticated, IsOwnerUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all().order_by('-timestamp')
    serializer_class = ApartmentSerializer

    # Set permission for only user owner apartment can edit it.
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerApartmentOrReadOnly]

    # Use filter_backends inherit from GenericAPIView
    filter_backends = [filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter]
    # Add search by 'address', filter by 'category', 'district' and ordering by 'price'
    filterset_class = ApartmentFilter
    search_fields = ['address']
    ordering_fields = ('price',)

    # fill current username when create new apartment
    # Use perform_create inherit from CreateModelMixin
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    # List all apartments available
    def list(self, request, *args, **kwargs):
        # Given a queryset, filter it with whichever filter backend is in use.
        queryset = self.filter_queryset(self.queryset.filter(issold=False))
        # Pagination for the results
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # Add extra action and routing /apartment/sold
    @action(detail=False, url_path='sold')
    def sold(self, request, format=None):
        # Given a queryset, filter it with whichever filter backend is in use.
        queryset = self.filter_queryset(
            self.queryset.filter(issold=True))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-timestamp')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Create a transaction and set issold = True for that Apartment
    def perform_create(self, serializer):
        transaction = serializer.save(buyer=self.request.user)
        transaction.apartment.issold = True
        transaction.apartment.save()


