from django.core.management.base import BaseCommand
from apps.projects.models import Task, Statuses, Priorities


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # random_tasks = Task.objects.order_by('?')[:5]
        # for task in random_tasks:
        #     task.priority = Priorities.URGENT
        #     task.save()
        # the_task = Task.objects.get(description='Art trade interview speak positive half choose.')
        # the_task.priority = Priorities.URGENT
        # the_task.save()
        all_tasks = Task.objects.filter(status=Statuses.NEW, priority=Priorities.URGENT)
        print(*(f'{task.name}, {task.status}, {task.priority}, {task.due_date}, {task.assignee.email}' for task in all_tasks), sep='\n')

