from django.core.management.base import BaseCommand
from apps.projects.models import Task, Statuses


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        specific_task = Task.objects.filter(name__exact='everything'
                ).update(status=Statuses.PENDING)
        if not specific_task:
            return 'Nothing found.'
        return None

