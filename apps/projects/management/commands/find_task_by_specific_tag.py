from django.core.management.base import BaseCommand
from apps.projects.models import Task


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        matched = Task.objects.filter(tags__name__icontains='I/CD')
        print(*(f'{task.name} {task.status} {task.priority} {task.project.name}' for task in matched), sep='\n')

