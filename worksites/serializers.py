from rest_framework import serializers
from .models import Worksites, CollabWorksites

class CollabWorksitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollabWorksites
        fields = "__all__"

class WorksiteSerializer(serializers.ModelSerializer):
    collaborations = CollabWorksitesSerializer(many=True, read_only=True)

    class Meta:
        model = Worksites
        fields = ['id', 'image', 'name', 'address', 'lat', 'lon', 'is_open', 'net_worth', 'financier', 'contractor_id', 'link', 'date', 'date_update', 'type', 'collaborations']