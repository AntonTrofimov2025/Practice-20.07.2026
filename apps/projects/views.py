from rest_framework import status
from apps.projects.serializers.project import ProjectSerializer
from rest_framework.decorators import api_view
from apps.projects.models import Project
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

@api_view(['GET'])
def get_all_projects(request):
    project_name = request.query_params.get('name')
    all_projects = Project.objects.all()
    if project_name:
        all_projects = all_projects.filter(name=project_name)
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

