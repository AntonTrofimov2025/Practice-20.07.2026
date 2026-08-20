from rest_framework import serializers
from apps.projects.models import Project, ProjectFile
from apps.projects.utils.upload_file_helpers import validate_extension, validate_file_size
from apps.projects.utils.upload_file_helpers import create_path
from config.settings import MEDIA_ROOT

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'count_of_files']
        read_only_fields = ['count_of_files']

class AllProjectFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ['id', 'name', 'file', 'created_at', 'projects']

class DownloadsFileSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(use_url=True)

    class Meta:
        model = ProjectFile
        fields = ['id', 'name', 'file', 'attachment']

class CreateProjectFileSerializer(serializers.ModelSerializer):
    # file = serializers.FileField(validators=[validate_extension, validate_file_size])

    class Meta:
        model = ProjectFile
        fields = ['id', 'name', 'file', 'created_at', 'projects']

    def validate_name(self, value):
        if not value.isascii():
            raise serializers.ValidationError('File name is not in ASCII!')
        return value

    def create(self, validated_data):
        create_path(MEDIA_ROOT / 'projects')

        return super().create(validated_data)

