from rest_framework import serializers
from .models import Directory, File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'extension', 'size', 'mime_type', 'date']

class DirectorySerializerChildren(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    files = FileSerializer(read_only=True, many=True)

    class Meta:
        model = Directory
        fields = ['id', 'name', 'parent', 'worksite', 'children', 'files']

    def get_field_names(self, declared_fields, info):
        depth = self.context.get('depth', 0)
        if depth >= 2:  # Limita la profondità della ricorsione a 2
            return ['id', 'name']
        return super().get_field_names(declared_fields, info)

    def get_parent(self, obj):
        if obj.parent:
            return DirectorySerializer(obj.parent, context={'depth': self.context.get('depth', 0) + 1}).data
        return None

    def get_children(self, obj):
        if obj.subdirectories.all().exists():
            return DirectorySerializerNoParent(obj.subdirectories.all(), many=True, context={'depth': self.context.get('depth', 0) + 1}).data
        return []
    

class DirectorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Directory
        fields = ['id', 'name', 'parent', 'worksite']

    def get_field_names(self, declared_fields, info):
        depth = self.context.get('depth', 0)
        if depth >= 2:  # Limita la profondità della ricorsione a 2
            return ['id', 'name']
        return super().get_field_names(declared_fields, info)

    def get_parent(self, obj):
        if obj.parent:
            return DirectorySerializer(obj.parent, context={'depth': self.context.get('depth', 0) + 1}).data
        return None

class DirectorySerializerNoParent(serializers.ModelSerializer):

    class Meta:
        model = Directory
        fields = ['id', 'name', 'worksite']