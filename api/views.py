from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Task
from api.serializers import TaskSerializer
from rest_framework import status


@api_view(['GET'])
def get_tasks(request):
    tasks = Task.objects.filter(is_deleted=False, checked=False)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=200)

@api_view(['PUT'])
def update_tasks(request):
    task_id = request.query_params.get('id')
    task = Task.objects.get(id=task_id)

    name = request.data.get('name', None)

    if name:
        task.name = name
        task.save()

    return Response({'message': 'Task modificato con successo'}, status=200)

@api_view(['GET'])
def history_tasks(request):
    tasks = Task.objects.filter(is_deleted=True, checked=True)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def new_task(request):
    name = request.data.get('name')
    if name:
        task = Task.objects.create(name=name)

    return Response({'message': 'Task aggiunto con successo'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def delete_tasks(request):
    task_id = request.data.get('id')
    
    if not task_id:
        return Response({'error': 'ID non fornito'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        task = Task.objects.get(id=task_id)
        task.is_deleted = True
        task.checked = True
        task.save()
        return Response({'message': 'Task eliminato con successo'}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({'error': 'Task non trovato'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Raccogli dettagli sull'errore per il debug
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)