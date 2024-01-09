import django_filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ContactGroup, ContactActivityLog
from .serializers import ContactGroupSerializer
from django_filters import rest_framework as filters
from .models import Contact
from .serializers import ContactSerializer
from rest_framework import viewsets, permissions


class ContactFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')

    class Meta:
        model = Contact
        fields = ['first_name', 'city']


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ContactFilter
    search_fields = ['first_name', 'last_name', 'city', 'country', 'street']
    permission_classes = [permissions.AllowAny]


class ContactGroupViewSet(viewsets.ModelViewSet):
    queryset = ContactGroup.objects.all()
    serializer_class = ContactGroupSerializer
