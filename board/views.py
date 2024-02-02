from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Boards
from .serializers import BoardsSerializer
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allows clients to dynamically adjust page size

class BoardsListView(ListAPIView):
    queryset = Boards.objects.all()
    serializer_class = BoardsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'body', 'author']  # Aggiusta secondo le necessità
    filterset_fields = ['worksite', 'apartment', 'type']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset