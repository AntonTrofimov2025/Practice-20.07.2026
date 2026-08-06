from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from apps.projects.models import Tag
from apps.projects.serializers import TagSerializer


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

