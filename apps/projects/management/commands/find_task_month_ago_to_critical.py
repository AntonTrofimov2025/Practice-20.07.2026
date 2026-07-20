from django.core.management.base import BaseCommand
from apps.projects.models import Task, Priorities
from django.utils import timezone
from datetime import datetime, timedelta
import calendar


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        month_ago = timezone.now() - timedelta(weeks=5)
        _, last_month_day = calendar.monthrange(month_ago.year, month_ago.month)
        filtered_tasks = Task.objects.filter(project__name='picture',
                                             created_at__range=(datetime(month_ago.year, month_ago.month, 1),
                                             datetime(month_ago.year, month_ago.month, last_month_day)))
        if not filtered_tasks.exists():
            return self.stdout.write("Задачи за прошлый месяц не найдены.")
        filtered_tasks.update(priority=Priorities.CRITICAL)
        print(*((task.name, task.project.name) for task in filtered_tasks), sep='\n')
        return None

