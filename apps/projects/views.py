from rest_framework import status
from apps.projects.serializers import (ProjectSerializer,
                                       TaskSerializer,
                                TaskCreateUpdateSerializer,
                                       TagSerializer,
                                       TaskInfoSerializer)
from rest_framework.decorators import api_view
from apps.projects.models import Project, Task, Tag
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

@api_view(['GET'])
def get_all_projects(request):
    project_name = request.query_params.get('name')
    all_projects = Project.objects.all()
    if project_name:
        all_projects = all_projects.filter(name__icontains=project_name)
    serialize_data = ProjectSerializer(all_projects, many=True)
    return Response(data=serialize_data.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_project_by_id(request, pk):
    # try:
    #     project = Project.objects.get(id=pk)
    #     serialize = ProjectSerializer(project)
    #     return Response(serialize.data, status=status.HTTP_200_OK)
    # except Project.DoesNotExist:
    #     return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    project = get_object_or_404(Project, id=pk)
    serializer = ProjectSerializer(project)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_tasks(request):
    specific_project = request.query_params.get('project')
    all_tasks = Task.objects.all()
    if specific_project:
        all_tasks = all_tasks.filter(project__name__icontains=specific_project)
    serializer = TaskSerializer(all_tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_task_by_id(request, pk):
    task_by_id = get_object_or_404(Task, id=pk)
    serializer = TaskSerializer(task_by_id)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def post_task(request):
    serializer = TaskCreateUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def post_task_by_name(request):
#     project = get_object_or_404(Project, name=request.data['project'])
#     request_data = request.data.copy()
#     request_data['project'] = project.id
#     serializer = TaskCreateUpdateSerializer(data=request_data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def post_or_show_all_tags(request):
    if request.method == 'GET':
        all_tags = Tag.objects.all()
        serializer = TagSerializer(all_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': f"New Tag '{serializer.data['name']}' has been created :)"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def get_or_upd_tag_by_id(request, pk):
    tag_by_id = get_object_or_404(Tag, id=pk)
    if request.method == 'GET':
        serializer = TagSerializer(tag_by_id)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        tag_by_id.delete()
        return Response({'msg': f"Tag {pk} has been successfully deleted :)"}, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = TagSerializer(tag_by_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': f"Tag {serializer.data['name']} ({pk}) has been successfully updated :)"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_task_info(request, pk):
    task_by_id = get_object_or_404(Task, id=pk)
    serializer = TaskInfoSerializer(task_by_id)
    return Response(serializer.data, status=status.HTTP_200_OK)

