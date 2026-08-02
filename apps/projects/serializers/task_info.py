from rest_framework import serializers
from apps.projects.models import Task
from .tags import TagSerializer


class TaskInfoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Task
        fields = ['id',
                 'name',
                 'status',
                 'priority',
                 'tags',
                 'project',
                 'created_at',
                 'due_date']

