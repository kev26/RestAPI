from django.contrib import admin
from .models import Apartment, Transaction, User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'seller', 'address', 'district', 'arena',
                    'price', 'description', 'issold')
    list_filter = ('issold',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'apartment')
