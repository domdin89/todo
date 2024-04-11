from rest_framework import serializers
from .models import Directory, File

def get_file_path(file_id):
    try:
        file = File.objects.get(id=file_id)
        return "media/private/" + file.file.name
    except File.DoesNotExist:
        return None
    
class FileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'name', 'extension', 'size', 'mime_type', 'date', 'url']

    def get_url(self, obj):
        # Here you can implement logic similar to your `get_file` function
        # For example, using boto3 to generate a signed URL for the file object.
        import boto3
        from django.conf import settings

        # Assume get_file_path is a function that retrieves the S3 path for the file
        file_path = get_file_path(obj.id)
        
        s3_client = boto3.client(
            's3',
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        
        # Generate the signed URL
        signed_url = s3_client.generate_presigned_url(
            'get_object', 
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': file_path}, 
            ExpiresIn=3600  # URL valid for 1 hour
        )
        
        return signed_url
    
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
    

class DirectorySerializerChildrenMain(serializers.ModelSerializer):
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
        # Filter subdirectories to exclude those with apartment_id != None
        child_directories = obj.subdirectories.filter(apartment_id=None)
        if child_directories.exists():
            return DirectorySerializerNoParent(child_directories, many=True, context={'depth': self.context.get('depth', 0) + 1}).data
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