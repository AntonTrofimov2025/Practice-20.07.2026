from django.core.management.base import BaseCommand
from apps.projects.models import Task, Priorities
from django.db.models import F
from django.utils import timezone
from datetime import datetime, timedelta, date
from faker import Faker

fake = Faker()



class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        filtered_tasks = Task.objects.filter(assignee__isnull=True)
        print(*(f'{task.name} {task.project.name}' for task in filtered_tasks), sep='\n')


