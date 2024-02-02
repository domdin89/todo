from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClientApartmentsSerializer
from .models import ClientApartments
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allows clients to dynamically adjust page size

class ClientApartmentsListView(ListAPIView):
    queryset = ClientApartments.objects.all().select_related('apartment')
    serializer_class = ClientApartmentsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['profile__first_name', 'profile__last_name']  # Adjust based on search requirements

    def get_queryset(self):
        queryset = super().get_queryset()
        worksite = self.request.query_params.get('worksite')
        if worksite:
            queryset = queryset.filter(apartment__worksite__id=worksite)
        return queryset