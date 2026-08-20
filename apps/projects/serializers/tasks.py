from rest_framework import serializers
from apps.projects.models import Task, Project
from . import ProjectSerializer
from django.contrib.auth import get_user_model


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'priority', 'assignee', 'project']
        read_only_fields = ['id', 'assignee', 'project']

class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')
    assignee = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field='email')

    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'priority', 'assignee', 'project']
        read_only_fields = ['id']

class TaskDetailSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Task
        exclude = ['updated_at', 'deleted_at', ]

