from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from worksites.models import Worksites
from .models import Boards, BoardsRecipient
from .serializers import BoardRecipientSerializer, BoardsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from django.shortcuts import get_object_or_404

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allows clients to dynamically adjust page size

class BoardsListView(ListCreateAPIView):
    queryset = Boards.objects.all()
    serializer_class = BoardsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'author']  # Aggiustato per corrispondere al YAML
    filterset_fields = ['type']

    def get_queryset(self):
        queryset = super().get_queryset()
        order_param = self.request.GET.get('order', 'desc')
        order_by_field = self.request.GET.get('order_by', 'id')  # Prendi il campo da 'order_by', default a 'id'
        
        # Applica direttamente l'ordinamento
        if order_param == 'desc':
            queryset = queryset.order_by('-' + order_by_field)  # Ordinamento discendente
        else:
            queryset = queryset.order_by(order_by_field)  # Ordinamento ascendente
        
        return queryset


class BoardsWorksiteListView(ListCreateAPIView):
    serializer_class = BoardRecipientSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['board__title', 'board__body']
    ordering_fields = ['id', 'date', 'date_update']
    filterset_fields = ['recipient_type']  # Assuming you want to filter by recipient_type

    def get_queryset(self):
        worksite_id = self.request.GET.get('worksite')
        worksite = get_object_or_404(Worksites, pk=worksite_id)
        queryset = BoardsRecipient.objects.filter(recipient_type='WORKSITE', worksites=worksite)

        return queryset