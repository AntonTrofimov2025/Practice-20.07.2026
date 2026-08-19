from rest_framework import serializers
from apps.projects.models import Task
from . import ProjectSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'priority']
        read_only_fields = ['id']


class TaskDetailSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Task
        exclude = ['updated_at', 'deleted_at', ]

