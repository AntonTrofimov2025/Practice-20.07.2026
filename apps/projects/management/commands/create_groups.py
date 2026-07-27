from django.core.management.base import BaseCommand
from apps.projects.models import Project, Task, Tag, Statuses, Priorities
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from config.settings import ROLE_PERMISSION
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):

    @staticmethod
    def add_permission(group, permissions: list[tuple[str, str, str]] | tuple[str, str, str]):
        if isinstance(permissions, tuple):
            permissions = [permissions]
        for key, value, command in permissions:
            group_content_type = ContentType.objects.get(app_label=key.lower(),
                                                         model=value.lower())
            # for view_group_permission in Permission.objects.filter(content_type=group_content_type):
            #     if command in view_group_permission.name:
            #         group.permissions.add(view_group_permission)
            matched_permissions = Permission.objects.filter(content_type=group_content_type,
                                                            codename__icontains=command.lower())
            group.permissions.add(*matched_permissions)

    @staticmethod
    def create_permission():
        for key, value in ROLE_PERMISSION.items():
            group, _ = Group.objects.get_or_create(name=key)
            permission_list = [tuple(permission.split('.')) for permission in value]
            Command.add_permission(group, permission_list)

    def handle(self, *args, **kwargs):
        # import pdb; pdb.set_trace() # For debugging reasons, s(Step), r(Return), n(Next)
        # managers_group, _ = Group.objects.get_or_create(name='Managers')
        # clients_group, _ = Group.objects.get_or_create(name='Clients')
        # developers_group, _ = Group.objects.get_or_create(name='Developers')

        self.create_permission()

        # self.add_permission(managers_group, [('auth', 'group'),
        #                                      ('auth', 'user'),
        #                                      ('auth', 'permission'),
        #                                      ('projects', 'tag'),
        #                                      ('projects', 'task')])

        # Разрешения и Пользователи (встроенное приложение 'auth')
        # ('auth', 'view_permission'),  # Просматривать все разрешения
        # ('auth', 'add_permission'),  # Добавлять новые разрешения ('auth', 'add_user'),
        # Добавлять новых пользователей ('auth', 'view_user'),
        # Просматривать всех пользователей # Проекты (Замените 'myapp' на имя вашего Django-приложения)
        # ('myapp', 'add_project'),  # Создавать проекты ('myapp', 'change_project'),
        # Изменять проекты ('myapp', 'delete_project'),
        # Удалять проекты('myapp', 'view_project'),
        # Просматривать проекты # Файлы проектов ('myapp', 'add_projectfile'),
        # Создавать файлы ('myapp', 'change_projectfile'),
        # Изменять файлы ('myapp', 'delete_projectfile'),
        # Удалять файлы ('myapp', 'view_projectfile'),
        # Просматривать файлы # Тэги ('myapp', 'add_tag'),
        # Добавлять тэги ('myapp', 'change_tag'),
        # Изменять тэги ('myapp', 'view_tag'),
        # Просматривать тэги # Задачи ('myapp', 'add_task'),
        # Добавлять задачи ('myapp', 'change_task')