from django.core.management.base import BaseCommand
from apps.projects.models import Task, Statuses


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        old_tasks = Task.objects.filter(status=Statuses.NEW)
        print(*(f'OLD STATUS: {task.status}' for task in old_tasks))
        updated_tasks = old_tasks.update(status=Statuses.IN_PROGRESS)
        print(f'UPDATED: {updated_tasks}')

