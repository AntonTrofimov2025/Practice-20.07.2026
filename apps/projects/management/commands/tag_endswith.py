from django.core.management.base import BaseCommand
from apps.projects.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        found_tags = Tag.objects.filter(name__endswith='task')
        if not found_tags:
            return 'Matches not found!'
        for tag in found_tags:
            self.stdout.write(str(tag))
        return None