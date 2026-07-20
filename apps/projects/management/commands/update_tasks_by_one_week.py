from django.core.management.base import BaseCommand
from apps.projects.models import Task, Priorities
from django.db.models import F
from django.utils import timezone
from datetime import datetime, timedelta, date
from faker import Faker

fake = Faker()



class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # none_due_date = Task.objects.filter(due_date__isnull=True).all()
        # for task in none_due_date:
        #     task.due_date = fake.date_between_dates(date(2026, 8, 1),
        #                                             date(2027, 1, 1))
        #     task.save()
        Task.objects.all().update(due_date=F('due_date') + timedelta(weeks=1))