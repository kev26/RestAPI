from django_filters import FilterSet, RangeFilter
from .models import Apartment


class ApartmentFilter(FilterSet):
    price = RangeFilter()
    class Meta:
        model = Apartment
        fields = (
            'category', 'district', 'price'
        )
        
