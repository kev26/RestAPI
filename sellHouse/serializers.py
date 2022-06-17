from rest_framework import serializers
from .models import User, Apartment, Transaction
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import UserCreateSerializer


class UserSerializer(serializers.ModelSerializer):
    apartment = serializers.StringRelatedField(
        many=True, required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'phone',
            'apartment'
        ]


class ApartmentSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Apartment
        fields = [
            'id',
            'seller',
            'address',
            'arena',
            'price',
            'description',
            'timestamp'
        ]


class TransactionSerializer(serializers.ModelSerializer):
    # Show name buyer
    buyer = serializers.ReadOnlyField(source='buyer.username')

    class Meta:
        model = Transaction
        fields = [
            'id', 
            'buyer', 
            'apartment', 
            'timestamp'
        ]