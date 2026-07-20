from django.core.management.base import BaseCommand
from apps.projects.models import Project
from datetime import datetime
from django.utils import timezone


filter_date = timezone.make_aware(datetime(2025, 2, 7))


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        projects_by_date = Project.objects.filter(created_at__gt=filter_date)
        files_in_projects = [project for project in projects_by_date
                             if len(project.files.all()) >= 3]
        print(*((project, *(file.name for file in project.files.all())) for project in files_in_projects), sep='\n')

