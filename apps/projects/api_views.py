from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from apps.projects.models import Tag, Project, ProjectFile, Task
from apps.projects.serializers import (TagSerializer, ProjectSerializer,
                            AllProjectFilesSerializer, CreateProjectFileSerializer,
                                       TaskSerializer, TaskDetailSerializer,
                                       TaskCreateUpdateSerializer)
from datetime import datetime, timedelta
from django.utils import timezone


class TaskDetailAPIView(APIView):

    def get_task(self, pk):
        return get_object_or_404(Task, pk=pk)

    def get(self, request, pk):
        task = self.get_task(pk)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, partial=False):
        task = self.get_task(pk)
        serializer = TaskCreateUpdateSerializer(task, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        return self.put(request, pk, partial=True)

    def delete(self, request, pk):
        task = self.get_task(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

        if project_name := request.query_params.get('name'):
            all_projects = all_projects.filter(name__icontains=project_name)

        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if date_from and date_to:
            try:
                # date_from = datetime.strptime(date_from, '%d-%m-%Y').astimezone()
                # date_to = datetime.strptime(date_to, '%d-%m-%Y').astimezone() + timedelta(hours=23, minutes=59, seconds=59)
                date_from = timezone.make_aware(datetime.strptime(date_from, '%d-%m-%Y'))
                date_to = timezone.make_aware(datetime.strptime(date_to, '%d-%m-%Y'))

                # all_projects = all_projects.filter(created_at__gte=date_from, created_at__lte=date_to)
                all_projects = all_projects.filter(created_at__date__range=(date_from.date(), date_to.date()))
            except ValueError:
                return Response(
                    {"error": "Incorrect date format. Use DD-MM-YYYY (for instance, 12-12-2024)"},
                    status=status.HTTP_400_BAD_REQUEST
                )

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

class ProjectFileListAPIView(APIView):

    def get(self, request):
        all_pr_files = ProjectFile.objects.prefetch_related('projects').all()

        if name := request.query_params.get('name'):
            all_pr_files = all_pr_files.filter(name=name)

        serializer = AllProjectFilesSerializer(all_pr_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateProjectFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProjectFileDetailAPIView(APIView):

    def get(self, request, pk):
        pr_file = get_object_or_404(ProjectFile, pk=pk)
        serializer = AllProjectFilesSerializer(pr_file)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, partial=False):
        pr_file = get_object_or_404(ProjectFile, pk=pk)
        serializer = CreateProjectFileSerializer(pr_file, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        return self.put(request, pk, partial=True)

    def delete(self, request, pk):
        pr_file = get_object_or_404(ProjectFile, pk=pk)
        pr_file.delete()
        import os
        from config.settings import MEDIA_ROOT, MEDIA_PROJECTS
        try:
            os.remove(MEDIA_ROOT / MEDIA_PROJECTS / pr_file.name)
        except FileNotFoundError:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)