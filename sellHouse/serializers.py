from rest_framework import serializers
from .models import User, Apartment, Transaction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    apartment = serializers.HyperlinkedRelatedField(
        many=True, view_name='apartment-detail', read_only=True)

    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'email',
            'phone',
            'apartment'
        ]


class ApartmentSerializer(serializers.HyperlinkedModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Apartment
        fields = [
            'url',
            'seller',
            'address',
            'arena',
            'price',
            'description',
            'timestamp'
        ]


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    buyer = serializers.ReadOnlyField(source='buyer.username')
    apartment_sold = serializers.HyperlinkedRelatedField(view_name='sold-detail', read_only=True)
    class Meta:
        model = Transaction
        fields = [
            'id',
            'buyer',
            'apartment_sold',
            'apartment',
            'timestamp'
        ]