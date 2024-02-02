from rest_framework import serializers
from .models import Boards
from .models import Boards

class BoardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boards
        fields = ['id', 'worksite', 'apartment', 'image', 'title', 'body', 'author', 'date', 'date_update', 'recipients', 'type']
        extra_kwargs = {
            'image': {'required': False},
            'recipients': {'required': False},
            'type': {'required': False}
        }
