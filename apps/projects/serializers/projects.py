from rest_framework import serializers
from apps.projects.models import Project, ProjectFile
from apps.projects.utils.upload_file_helpers import validate_extension, validate_file_size

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'created_at']

class AllProjectFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ['id', 'name', 'file', 'created_at', 'projects']


class CreateProjectFileSerializer(serializers.ModelSerializer):
    # file = serializers.FileField(validators=[validate_extension, validate_file_size])

    class Meta:
        model = ProjectFile
        fields = ['id', 'name', 'file', 'created_at', 'projects']

    def validate_name(self, value):
        if not value.isascii():
            raise serializers.ValidationError('File name is not in ASCII!')
        return value

    # def create(self, validated_data):
    #     if validated_data
    #
    #     return super().create(validated_data)

