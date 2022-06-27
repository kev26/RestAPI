from django_filters import FilterSet
from .models import Apartment


class ApartmentFilter(FilterSet):
    class Meta:
        model = Apartment
        fields = {
            'price': ['lt','gt']
        }
