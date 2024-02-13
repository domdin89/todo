from rest_framework import serializers
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from apartments.models import Apartments
from apartments.serializers import ApartmentSerializer
from worksites.models import Worksites

from worksites.serializers import WorksiteStandardSerializer
from .models import Boards, BoardsRecipient

class RecipientsSerializer(serializers.ModelSerializer):
    worksite = serializers.SlugRelatedField(
        queryset=Worksites.objects.all(), slug_field='id', source='worksite_id', read_only=True)
    apartment = serializers.SlugRelatedField(
        queryset=Apartments.objects.all(), slug_field='id', source='apartment_id', read_only=True)
    profile = serializers.SlugRelatedField(
        queryset=Profile.objects.all(), slug_field='id', source='profile_id', read_only=True)

    class Meta:
        model = BoardsRecipient
        fields = ['id', 'worksite', 'apartment', 'profile', 'worksite_id', 'apartment_id', 'profile_id']
        extra_kwargs = {
            'worksite_id': {'write_only': True},
            'apartment_id': {'write_only': True},
            'profile_id': {'write_only': True},
        }


class BoardsSerializer(serializers.ModelSerializer):
    recipients = RecipientsSerializer(many=True)

    class Meta:
        model = Boards
        fields = ['id', 'image', 'title', 'body', 'author', 'date', 'date_update', 'type', 'recipients']

    def create(self, validated_data):
        recipients_data = validated_data.pop('recipients', [])
        board = Boards.objects.create(**validated_data)
        for recipient_data in recipients_data:
            # Estrai i dati dei campi nidificati dopo la popolazione della chiave esterna 'board'
            recipient_data = recipient_data.get('recipients') if 'recipients' in recipient_data else recipient_data
            BoardsRecipient.objects.create(board=board, **recipient_data)
        return board