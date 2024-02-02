from rest_framework import serializers
from .models import Worksites, CollabWorksites
from accounts.models import Profile
from accounts.serializers import ProfileSerializer

class CollabWorksitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollabWorksites
        fields = "__all__"

class WorksiteSerializer(serializers.ModelSerializer):
    collaborations = CollabWorksitesSerializer(many=True, read_only=True)

    class Meta:
        model = Worksites
        fields = ['id', 'image', 'name', 'address', 'lat', 'lon', 'is_open', 'net_worth', 'financier', 'contractor_id', 'link', 'date', 'date_update', 'collaborations']


class GetCollabWorksitesSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())


    class Meta:
        model = CollabWorksites
        fields = "__all__"

class WorksiteStandardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worksites
        fields = ['id']


class WorksiteProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = CollabWorksites
        fields = ['profile', 'worksite', 'role', 'order']