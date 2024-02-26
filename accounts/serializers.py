from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.db.models import CharField
from django.db.models.functions import Concat
from accounts.models import Profile
from worksites.models import CollabWorksites

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        try:
            profile = Profile.objects.get(user=user)
            token['profile_id'] = profile.id
        except Profile.DoesNotExist:
            pass  # Handle the case if the profile is not found

        return token



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id','user', 'first_name', 'last_name', 'mobile_number', 'email', 
             'type', 'image', 'token', 'is_active', 'date', 'date_update'
        ]
        extra_kwargs = {
            'image': {'required': False},
        }
    
class ProfileSerializerRole(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id','user', 'first_name', 'last_name', 'mobile_number', 'email', 
             'type', 'image', 'token', 'is_active', 'date', 'date_update'
        ]
        extra_kwargs = {
            'image': {'required': False},
        }
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Rimuovi date_end se è nullo
        for role in data['roles_with_dates']:
            if role['date_end'] is None:
                role.pop('date_end', None)
        return data

class WorksiteProfileSerializerNew(serializers.ModelSerializer):
    
    class Meta:
        model = CollabWorksites
        fields = '__all__'
class ProfileSerializerNew(serializers.ModelSerializer):
    collabworksites = WorksiteProfileSerializerNew(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'first_name', 'last_name', 'mobile_number', 'email', 
            'type', 'image', 'token', 'is_active', 'date', 'date_update', 'collabworksites',
        ]
        extra_kwargs = {
            'image': {'required': False},
        }
