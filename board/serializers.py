from rest_framework import serializers
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from apartments.models import Apartments
from apartments.serializers import ApartmentSerializer
from worksites.models import Worksites

from worksites.serializers import WorksiteStandardSerializer
from .models import Boards, BoardsRecipient

class RecipientsSerializer(serializers.ModelSerializer):
    # For read operations, use SlugRelatedField or SerializerMethodField to represent the related object in a readable format
    worksites_detail = serializers.SlugRelatedField(slug_field='name', read_only=True, source='worksites')
    apartment_detail = serializers.SlugRelatedField(slug_field='name', read_only=True, source='apartment')
    profile_detail = serializers.SlugRelatedField(slug_field='first_name', read_only=True, source='profile')
    class Meta:
        model = BoardsRecipient
        fields = ['id', 'worksite_id', 'apartment_id', 'profile_id', 'worksites_detail', 'apartment_detail', 'profile_detail']
        extra_kwargs = {
            'worksites_id': {'write_only': True, 'queryset': Worksites.objects.all()},
            'apartment_id': {'write_only': True, 'queryset': Apartments.objects.all()},
            'profile_id': {'write_only': True, 'queryset': Profile.objects.all()},
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