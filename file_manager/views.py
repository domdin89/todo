from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Directory
from rest_framework.permissions import IsAdminUser
from .serializers import DirectorySerializerChildren  

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
