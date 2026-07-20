from django.core.management.base import BaseCommand
from apps.projects.models import Task, Statuses
from django.db.models import Q

# excluded_statuses = [status.value for status in Statuses
#                      if status.value in [Statuses.IN_PROGRESS, Statuses.PENDING, Statuses.BLOCKED]]
excluded_statuses = [Statuses.IN_PROGRESS, Statuses.PENDING, Statuses.BLOCKED]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        all_tasks = Task.objects.filter(~Q(status__in=excluded_statuses))
        print(*(f'Task: {task.name}, Status: {task.status}' for task in all_tasks), sep='\n')

