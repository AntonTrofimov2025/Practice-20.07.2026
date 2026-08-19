from rest_framework import serializers
from apps.projects.models import Task, Project
from . import ProjectSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'priority', 'assignee', 'project']
        read_only_fields = ['id', 'assignee', 'project']

class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')

    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'priority', 'assignee', 'project']
        read_only_fields = ['id']

class TaskDetailSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Task
        exclude = ['updated_at', 'deleted_at', ]

