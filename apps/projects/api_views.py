from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from apps.projects.models import Tag, Project
from apps.projects.serializers import TagSerializer, ProjectSerializer
from datetime import datetime, timedelta


class TagListCreateApiView(APIView):

    def get(self, request):
        all_tags = Tag.objects.all()
        serializer = TagSerializer(all_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TagDetailApiView(APIView):

    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, partial=False):
        tag = get_object_or_404(Tag, pk=pk)
        serializer = TagSerializer(tag, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        return self.put(request, pk, partial=True)

    def delete(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectListApiView(APIView):

    def get(self, request):
        all_projects = Project.objects.all()

        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if date_from and date_to:
            try:
                date_from = datetime.strptime(date_from, '%d-%m-%Y').astimezone()
                date_to = datetime.strptime(date_to, '%d-%m-%Y').astimezone() + timedelta(hours=23, minutes=59, seconds=59)

                all_projects = all_projects.filter(created_at__gte=date_from, created_at__lte=date_to)
            except Exception:
                pass

        serializer = ProjectSerializer(all_projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProjectDetailApiView(APIView):

    def get(self, request, pk):
        tag = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, partial=False):
        tag = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(tag, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        return self.put(request, pk, partial=True)

    def delete(self, request, pk):
        tag = get_object_or_404(Project, pk=pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

