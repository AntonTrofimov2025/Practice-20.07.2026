from django.core.management.base import BaseCommand
from apps.projects.models import Project, ProjectFile
from django.utils import timezone
from datetime import timedelta

creation_period = timezone.now() - timedelta(weeks=60) # Decided instead of one week.


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        matched_files = {file.name for file in ProjectFile.objects.filter(created_at__gte=creation_period)}
        matched_projects = Project.objects.filter(files__name__in=matched_files)
        print(*((project.name, project.created_at) for project in matched_projects), sep='\n')

