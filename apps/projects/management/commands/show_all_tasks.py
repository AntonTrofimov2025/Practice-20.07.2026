from django.core.management.base import BaseCommand
from apps.projects.models import Task



class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print(*(f'Task: {task.name}, tags: {task.tags.all()}' for task in Task.objects.all()), sep='\n')

