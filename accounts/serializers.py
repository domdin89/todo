from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.db.models import CharField
from django.db.models.functions import Concat
from django.contrib.auth.models import User
from accounts.models import Privacy, Profile


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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = [
            'id','user', 'first_name', 'last_name', 'mobile_number', 'email', 
             'type', 'image', 'token', 'is_active', 'date', 'date_update', 'collabworksites', 'email_visible', 'img_visible', 'phone_visible', 'need_change_password'
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


class PrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Privacy
        fields = '__all__'
