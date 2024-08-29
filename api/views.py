from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Task
from api.serializers import TaskSerializer

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

    serializer = TaskSerializer(task)
    return Response(serializer.data, status=200)

@api_view(['PUT'])
def delete_tasks(request):
    task_id = request.query_params.get('id')
    task = Task.objects.get(id=task_id)

    task.is_deleted = True
    task.checked = True
    task.save()

    return Response({'message': 'Task eliminato con successo'}, status=200)