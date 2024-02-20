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

class ProfileSerializerNew(serializers.ModelSerializer):
    roles_with_dates = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'first_name', 'last_name', 'mobile_number', 'email', 
            'type', 'image', 'token', 'is_active', 'date', 'date_update', 'roles_with_dates',
        ]
        extra_kwargs = {
            'image': {'required': False},
        }

    def get_roles_with_dates(self, obj):
        roles_dates = CollabWorksites.objects.filter(profile=obj)\
            .values('role', 'date_start', 'date_end').distinct()
        return [{'role': rd['role'], 'date_start': rd['date_start'], 'date_end': rd['date_end']} for rd in roles_dates]
