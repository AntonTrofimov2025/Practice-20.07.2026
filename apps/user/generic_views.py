from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework import mixins
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer, RegisterUserSerializer
from apps.projects.models import ProjectFile
from apps.projects.serializers import AllProjectFilesSerializer, DownloadsFileSerializer


class UserListGenericView(ListCreateAPIView):

    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer

    serializers = {
        'POST': RegisterUserSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.request.method, UserListSerializer)

    def get_queryset(self):
        if project := self.request.query_params.get('project'):
            self.queryset = self.queryset.filter(project__name=project)
        return self.queryset


class DownloadProjectFileView(RetrieveAPIView):

    queryset = ProjectFile.objects.all()
    # serializer_class = DownloadsFileSerializer

    def retrieve(self, request, *args, **kwargs):
        # import mimetypes
        # obj = self.get_object()
        # # path = obj.file.storage.base_location
        # content_type, encodings = mimetypes.guess_type(obj.file.path)
        # content_type = content_type or 'application/octet-stream'
        # file = open(obj.file.path, 'rb')
        # # file = DownloadsFileSerializer(data=request.data)
        # # file.is_valid()
        try:
            instance = self.get_object()
        except Http404:
            # return Response(status=status.HTTP_404_NOT_FOUND)
            raise Http404("File not found, we're sorry")

        # if instance.file.storage.exists(instance.file.name):
        #     raise Http404('File not found')


        file = instance.file.open('rb')
        return FileResponse(file, as_attachment=True, filename=instance.name,
                            # content_type=content_type
                            )
        # except FileNotFoundError:
        #     # return Response(status=status.HTTP_404_NOT_FOUND)
        #     raise Http404('File not found')

