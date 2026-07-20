import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management.base import BaseCommand
from apps.projects.models import Task, Priorities
from datetime import datetime
from django.utils import timezone
from django.db.models import Q, F
import calendar


now = timezone.now()
_, last_day = calendar.monthrange(now.year, now.month)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        filtered_tasks = Task.objects.filter((Q(priority=Priorities.CRITICAL) | Q(priority=Priorities.URGENT)) &
                                             Q(due_date__range=(now, datetime(now.year, now.month, last_day))))
        print(*((task.name, task.due_date)for task in filtered_tasks), sep='\n')

