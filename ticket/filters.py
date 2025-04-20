import django_filters
from .models import Ticket

class CustomerTicketFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    
    class Meta:
        model = Ticket
        fields = ['title', 'status']

class TicketQueueFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    
    class Meta:
        model = Ticket
        fields = ['title', 'priority']

class EngineerTicketFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    
    class Meta:
        model = Ticket
        fields = ['title', 'status', 'priority']