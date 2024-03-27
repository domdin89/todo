from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Directory, File
from rest_framework.permissions import IsAdminUser
from .serializers import DirectorySerializerChildren
import boto3
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings

@api_view(['GET'])
#@permission_classes([IsAdminUser])
def get_directories(request):
    """
    Restituisce le directory basate sull'ID di un worksite, con opzione di filtrare per parent_id.
    """
    worksite_id = request.query_params.get('worksite_id')
    parent_id = request.query_params.get('parent_id', None)

    if not worksite_id:
        return Response({"error": "worksite_id è richiesto."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if parent_id:
            directories = Directory.objects.filter(id=parent_id)
        else:
            directories = Directory.objects.filter(worksite_id=worksite_id)

        serializer = DirectorySerializerChildren(directories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_file_path(file_id):
    try:
        file = File.objects.get(id=file_id)
        return file.file.name
    except File.DoesNotExist:
        return None
    
@api_view(['GET'])
#@permission_classes([IsAdminUser])
def get_file(request):
    file_id = request.query_params.get('file_id')
    # Assumi di avere una funzione che recupera il percorso del file su S3 in base a file_id
    file_path = get_file_path(file_id)
    
    # Crea un client S3
    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name=settings.AWS_S3_REGION_NAME)
    
    # Genera l'URL firmato
    signed_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': file_path}, ExpiresIn=3600)  # URL valido per 1 ora
    
    return JsonResponse({'url': signed_url})