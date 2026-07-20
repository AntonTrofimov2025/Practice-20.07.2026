from django.core.management.base import BaseCommand
from apps.projects.models import Task, Statuses, Priorities
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        specific_tasks = Task.objects.filter(
            Q(status=Statuses.PENDING, priority=Priorities.MEDIUM) |
            ~Q(tags__name='Q&A')
        )
        print(*(f'{task.name} , {task.project} , {task.assignee.email}' for task in specific_tasks), sep='\n')