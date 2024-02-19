from rest_framework import serializers

from accounts.serializers import ProfileSerializer
from .models import Apartments, ClientApartments, ApartmentSub
from worksites.serializers import WorksiteSerializer

class ApartmentSerializer(serializers.ModelSerializer):
    worksite = WorksiteSerializer()

    class Meta:
        model = Apartments
        fields = '__all__'

class ApartmentSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentSub
        fields = '__all__'

class ApartmentBaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Apartments
        fields = '__all__'


class WorksiteApartmentsSerializer(serializers.ModelSerializer):
    worksite = WorksiteSerializer()

    class Meta:
        model = Apartments
        fields = '__all__'


class ClientApartmentsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    apartment = ApartmentSerializer(read_only=True)

    class Meta:
        model = ClientApartments
        fields = '__all__'