from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from worksites.models import FoglioParticella
from .serializers import ApartmentBaseSerializer, ClientApartmentsSerializer
from .models import ApartmentSub, Apartments, ClientApartments
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


@api_view(['PUT'])
#@parser_classes([MultiPartParser])
def update_apartment(request, id):  # Aggiunta dell'argomento worksite_id
    try:
        apartment = Apartments.objects.get(id=id)
    except Apartments.DoesNotExist:
        return Response("Appartamento non trovato", status=status.HTTP_404_NOT_FOUND)


    subs = ApartmentSub.objects.filter(apartment=apartment)

    for sub in subs:
        sub.is_valid = False
        sub.save()

    apartment_data = {
        'worksite_id': apartment.worksite.id,
        'floor': request.data.get('floor', None),
        'note': request.data.get('note', None),
        'owner': request.data.get('owner', None),
        'owner_phone': request.data.get('owner_phone', None),
        'owner_email': request.data.get('owner_email', None),
        'owner_cf': request.data.get('owner_cf', None),
    }

    apartment_data = {key: value for key, value in apartment_data.items() if value is not None}

    apartment = Apartments.objects.create(**apartment_data)

    # Creazione dei subappartamenti se presenti nel payload
    subs_data = request.data.get('subs', [])
    for sub_data in subs_data:
        foglio_particella_id = sub_data.get('foglio_particella_id', None)
        foglio_particella = None
        if foglio_particella_id:
            foglio_particella = FoglioParticella.objects.get(pk=foglio_particella_id)

        sub_data = {
            'foglio_particella': foglio_particella,
            'sub': sub_data.get('sub', None),
            'apartment': apartment,
        }

        sub_data = {key: value for key, value in sub_data.items() if value is not None}

        sub = ApartmentSub.objects.create(**sub_data)

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


@api_view(['POST'])
def new_apartment(request):  
    worksite_id = request.data.get('worksite_id', None)  
    
    if worksite_id is None:
        return Response("Il campo 'worksite_id' è obbligatorio.", status=status.HTTP_400_BAD_REQUEST)

    apartment_data = {
        'worksite_id': worksite_id,
        'floor': request.data.get('floor', None),
        'note': request.data.get('note', None),
        'owner': request.data.get('owner', None),
        'owner_phone': request.data.get('owner_phone', None),
        'owner_email': request.data.get('owner_email', None),
        'owner_cf': request.data.get('owner_cf', None),
    }

    apartment_data = {key: value for key, value in apartment_data.items() if value is not None}

    apartment = Apartments.objects.create(**apartment_data)

    # Creazione dei subappartamenti se presenti nel payload
    subs_data = request.data.get('subs', [])
    for sub_data in subs_data:
        foglio_particella_id = sub_data.get('foglio_particella_id', None)
        foglio_particella = None
        if foglio_particella_id:
            foglio_particella = FoglioParticella.objects.get(pk=foglio_particella_id)

        sub_data = {
            'foglio_particella': foglio_particella,
            'sub': sub_data.get('sub', None),
            'apartment': apartment,
        }

        sub_data = {key: value for key, value in sub_data.items() if value is not None}

        sub = ApartmentSub.objects.create(**sub_data)

    return Response("Sub aggiornato con successo", status=status.HTTP_200_OK)