from django.shortcuts import render
from rest_framework.decorators import api_view,parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from worksites.serializers import WorksiteSerializer
from .decorators import validate_token
from rest_framework.response import Response

from worksites.models import Worksites
from apartments.models import ClientApartments



# Create your views here.


@api_view(['GET'])
@validate_token
def worksites(request):
    profile_id = request.profile_id
    

    worksites = Worksites.objects.filter(apartments__clientapartments__profile_id=profile_id).distinct()


    serializer = WorksiteSerializer(worksites, many=True)

    return Response({'results': serializer.data})
