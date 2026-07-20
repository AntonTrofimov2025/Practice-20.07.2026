from django.core.management.base import BaseCommand
from apps.projects.models import Tag
import sys

# if len(sys.argv) != 3:
#     print("Использование: python manage.py find_tag_by_name <tag_name>")
#     sys.exit(1)
#
# tag_name = sys.argv[2]
#
#
# class Command(BaseCommand):
#     def handle(self, tag_name, *args, **kwargs):
#         if not Tag.objects.filter(name=tag_name).exists():
#             return 'This Tag doesn\'t exist!'
#         print(*Tag.objects.filter(name=tag_name))


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not Tag.objects.filter(name='Разработка UI-кита и редизайн макета').exists():
            return 'This Tag doesn\'t exist!'
        print(*Tag.objects.filter(name='Разработка UI-кита и редизайн макета'))
        return None

