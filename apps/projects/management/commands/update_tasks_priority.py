from django.core.management.base import BaseCommand
from apps.projects.models import Task, Priorities
from django.db.models import F
from datetime import datetime, timedelta



class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # random_tasks = Task.objects.order_by('?')[:5]
        # for task in random_tasks:
        #     task.due_date = updated_date
        #     task.save()
        Task.objects.filter(due_date__gt=F('created_at') + timedelta(days=15)).update(priority=Priorities.CRITICAL)