from django.core.management.base import BaseCommand
from apps.projects.models import Project


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        found_project = Project.objects.filter(name__icontains='ci')
        print(*(files for project in found_project for files in project.files.all()), sep='\n')