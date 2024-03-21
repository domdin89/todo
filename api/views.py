from django.shortcuts import render
from rest_framework.decorators import api_view

from accounts.views import login_without_password
from worksites.serializers import WorksiteSerializer
from .decorators import validate_token
from rest_framework.response import Response

from worksites.models import Worksites
from apartments.models import ApartmentAccessCode, ClientApartments



# Create your views here.


@api_view(['GET'])
@validate_token
def worksites(request):
    profile_id = request.profile_id
    worksites = Worksites.objects.filter(apartments__clientapartments__profile_id=profile_id).distinct()

    serializer = WorksiteSerializer(worksites, many=True)

    return Response({'results': serializer.data})



@api_view(['POST'])
def apartment_code_validator(request):
    pin = request.data.get('pin')

    if pin:
        access_code = ApartmentAccessCode.objects.get(pin=pin, is_valid=True)

        ClientApartments.objects.create(
            profile=access_code.profile,
            apartment=access_code.apartment,
            is_active=True,
        )

        jwt_token, access_token = login_without_password(access_code.profile) # type: ignore

        if str(access_token) and str(jwt_token):
            access_code.is_valid = False
            access_code.save()
        
        return Response({
            "access": str(access_token),
            "refresh": str(jwt_token),
        })