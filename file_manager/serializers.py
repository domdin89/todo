from rest_framework import serializers
from .models import Directory, File
from apartments.serializers import ApartmentBaseSerializer
from worksites.serializers import WorksiteStandardSerializer

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
        fields = ['id', 'name', 'extension', 'size', 'mime_type', 'date', 'url', 'visible_in_app']

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

class DirectorySerializerNoChildren(serializers.ModelSerializer):
    worksite = WorksiteStandardSerializer()
    apartment = ApartmentBaseSerializer()

    class Meta:
        model = Directory
        fields = ['id', 'name', 'parent', 'worksite', 'created_by', 'date',  'type', 'room', 'apartment']  # Aggiungi tutti i campi che vuoi includere

# SERIALIZER FATTO SOLO PER TECNICI VISIBLE IN APP
class DirectorySerializerChildrenApp(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()

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
        # Filtra i subdirectories per includere solo quelli senza un apartment associato
        if obj.subdirectories.filter().exists():
            return DirectorySerializerNoChildren(obj.subdirectories.filter(apartment=obj.apartment), many=True, context=self.context).data
        return []
    
    def get_files(self, obj):
        files = File.objects.filter(directory_id=obj.id, visible_in_app=True)
        serializer = FileSerializer(files, many=True)
        return serializer.data

# SERIALIZER FATTO SOLO PER STAFF VISIBLE IN APP
class DirectorySerializerChildrenAppStaff(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()

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
        # Filtra i subdirectories per includere solo quelli senza un apartment associato
        if obj.subdirectories.filter().exists():
            return DirectorySerializerNoChildren(obj.subdirectories.filter(apartment=obj.apartment), many=True, context=self.context).data
        return []
    
    def get_files(self, obj):
        files = File.objects.filter(directory_id=obj.id)
        serializer = FileSerializer(files, many=True)
        return serializer.data
    

class DirectorySerializerChildren(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()

    class Meta:
        model = Directory
        fields = ['id', 'name', 'parent', 'worksite', 'children', 'files', 'type', 'room', 'apartment']

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
        # Filtra i subdirectories per includere solo quelli senza un apartment associato
        if obj.subdirectories.filter().exists():
            return DirectorySerializerNoChildren(obj.subdirectories.all(), many=True, context=self.context).data
        return []
    
    def get_files(self, obj):
        files = File.objects.filter(directory_id=obj.id)
        serializer = FileSerializer(files, many=True)
        return serializer.data
    

class DirectorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Directory
        fields = ['id', 'name', 'parent', 'worksite', 'type', 'room', 'apartment']

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


# QUESTO SERIALIZER FA VISUALIZZARE SOLO I FILE VISIBLE IN APP
class DirectorySerializerNew(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    #apartment = ApartmentBaseSerializer(read_only=True)
    files = serializers.SerializerMethodField()

    class Meta:
        model = Directory
        fields = ['id', 'name', 'parent', 'worksite', 'created_by', 'date', 'children', 'apartment', 'files', 'type']  # Aggiungi tutti i campi che vuoi includere

    def get_children(self, obj):
        # Filtra i subdirectories per includere solo quelli senza un apartment associato
        if obj.subdirectories.filter(apartment__isnull=True).exists():
            return DirectorySerializerNoChildren(obj.subdirectories.filter(apartment__isnull=True, worksite=obj.worksite), many=True, context=self.context).data
        return []

    def get_files(self, obj):
        files = File.objects.filter(directory_id=obj.id, visible_in_app=True)
        serializer = FileSerializer(files, many=True)
        return serializer.data



# QUESTO SERIALIZER FA VISUALIZZARE TUTTI I FILE PER STAFF
class DirectorySerializerNewStaff(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    #apartment = ApartmentBaseSerializer(read_only=True)
    files = serializers.SerializerMethodField()

    class Meta:
        model = Directory
        fields = ['id', 'name', 'parent', 'worksite', 'created_by', 'date', 'children', 'apartment', 'files', 'type']  # Aggiungi tutti i campi che vuoi includere

    def get_children(self, obj):
        # Filtra i subdirectories per includere solo quelli senza un apartment associato
        if obj.subdirectories.filter(apartment__isnull=True).exists():
            return DirectorySerializerNoChildren(obj.subdirectories.filter(apartment__isnull=True, worksite=obj.worksite), many=True, context=self.context).data
        return []

    def get_files(self, obj):
        files = File.objects.filter(directory_id=obj.id)
        serializer = FileSerializer(files, many=True)
        return serializer.data