import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    reference = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Payment 
        fields = ['reference']