from rest_framework import serializers

from accounts.serializers import ProfileSerializer
from .models import Apartments, ClientApartments, ApartmentSub
from worksites.serializers import FoglioParticellaSerializer, WorksiteSerializer

class ApartmentSerializer(serializers.ModelSerializer):
    worksite = WorksiteSerializer()

    class Meta:
        model = Apartments
        fields = '__all__'

class ApartmentSubSerializer(serializers.ModelSerializer):
    foglio_particella = FoglioParticellaSerializer(read_only=True)
    class Meta:
        model = ApartmentSub
        fields = '__all__'

class ApartmentBaseSerializer(serializers.ModelSerializer):
    subs = serializers.SerializerMethodField()
    
    class Meta:
        model = Apartments
        fields = ['id','worksite', 'floor', 'note', 'owner', 'owner_phone', 'owner_email', 'owner_cf', 'link', 'date', 'date_update', 'subs']


    def get_subs(self, obj):
        valid_subs = obj.subs.filter(is_valid=True, apartment_id=obj.id)
        
        return ApartmentSubSerializer(valid_subs, many=True).data 


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