from django.core.management.base import BaseCommand
from apps.projects.models import Project
from django.utils import timezone
from datetime import datetime
from django.db.models import Q

naive_date = datetime(year=2026, month=1, day=1)
above_date = timezone.make_aware(naive_date)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # (Project.objects.filter(name='especially').
        #  update(created_at=timezone.make_aware(datetime(2026, 3, 3))))
        projects_abv_date_n_match = Project.objects.filter(Q(created_at__gte=above_date) & Q(name__icontains='CI'))
        print('all matched projects:')
        for project in projects_abv_date_n_match:
            self.stdout.write(str((project.name, project.created_at)))

