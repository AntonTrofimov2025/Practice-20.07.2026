from django.core.management.base import BaseCommand
from apps.projects.models import Task, Statuses
from datetime import timedelta
from django.utils import timezone
from django.db.models import F


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        upd_tasks = Task.objects.filter(status=Statuses.IN_PROGRESS
                            ).update(due_date=F('due_date') + timedelta(days=3))
        print(f'UPD_COUNT: {upd_tasks}')

