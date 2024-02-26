from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApartmentBaseSerializer, ClientApartmentsSerializer
from .models import Apartments, ClientApartments
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view,parser_classes


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


class ApartmentListCreateAPIView(ListCreateAPIView):
    queryset = Apartments.objects.filter(is_active=True)
    serializer_class = ApartmentBaseSerializer
    #permission_classes = [IsAuthenticated]
    
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['owner']
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
            queryset = super().get_queryset()
            order_param = self.request.GET.get('order', 'desc')
            order_by_field = self.request.GET.get('order_by', 'id')
            worksite = self.request.GET.get('worksite')
            
            if order_param == 'desc':
                queryset = queryset.order_by('-' + order_by_field)
            else:
                queryset = queryset.order_by(order_by_field)
            
            if worksite:
                queryset = queryset.filter(worksite=worksite)  # Filtra per worksite se presente
        
            return queryset
          
    def list(self, request, *args, **kwargs):
        worksite = request.query_params.get('worksite')
        if not worksite:
            return Response({"status": "fail", "message": "Attenzione, worksite obbligatorio"}, status=status.HTTP_400_BAD_REQUEST)
        return super(ApartmentListCreateAPIView, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Handling multipart data including files
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['PUT'])
@parser_classes([MultiPartParser])
def update_apartment(request, id):  # Aggiunta dell'argomento worksite_id
    try:
        apartment = Apartments.objects.get(id=id)
    except Apartments.DoesNotExist:
        return Response("Appartamento non trovato", status=status.HTTP_404_NOT_FOUND)

    post_data = {
        'worksite': request.data.get('worksite', apartment.worksite),
        'floor': request.data.get('floor', apartment.floor),
        'note': request.data.get('note', apartment.note),
        'owner': request.data.get('owner', apartment.owner),
        'owner_phone': request.data.get('owner_phone', apartment.owner_phone),
        'owner_email': request.data.get('owner_email', apartment.owner_email),
        'owner_cf': request.data.get('owner_cf', apartment.owner_cf),
        'link': request.data.get('link', apartment.link),
        'is_active': request.data.get('is_active', apartment.is_active),

    }

    # Rimuovi i campi vuoti o non validi
    post_data = {key: value for key, value in post_data.items() if value is not None}

    # Aggiorna i campi del cantiere
    for key, value in post_data.items():
        setattr(apartment, key, value)

    # Salva il cantiere
    apartment.save()

    return Response("Appartamento aggiornato con successo", status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_apartment(request, id):
    try:
        apartment = Apartments.objects.get(id=id)
    except Apartments.DoesNotExist:
        return Response("Appartamento non trovato", status=status.HTTP_404_NOT_FOUND)

    apartment.is_active = False
    apartment.save()

    return Response("Appartamento rimosso", status=status.HTTP_200_OK)