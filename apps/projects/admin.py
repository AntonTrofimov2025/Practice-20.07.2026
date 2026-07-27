from django.contrib import admin
from apps.projects.models import (Project, Task,
                                  Tag, ProjectFile,
                                  Statuses, Priorities)
from django.db.models import F, Value
from django.db.models.functions import Replace



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'show_files_quantity')
    search_fields = ('name',)

    @admin.display(description='Files quantity')
    def show_files_quantity(self, projects):
        return projects.files.count()

    @admin.action(description='Replace all spaces to _ symbol')
    def replace_space_to__(self, request, projects):
        # for project in projects:
        #     project.name = project.name.replace(' ', '_')
        # projects.bulk_update(projects, ['name'])
        projects.update(name=Replace('name', Value(' '), Value('_')))

    actions = [replace_space_to__]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'status', 'priority', 'created_at', 'due_date', 'assignee')
    list_filter = ('project', 'status', 'priority', 'created_at', 'due_date', 'assignee')
    search_fields =('name',)

    @admin.action(description='Replace specific status to Done')
    def replace_status_to_done(self, request, tasks):
        tasks.update(status=Statuses.DONE)

    actions = [replace_status_to_done]


    priorities = [(priority.name, priority.value, priority.label) for priority in Priorities]
    for key, value, label in priorities:
        change_priority = lambda self, request, tasks, p=value: tasks.update(priority=p)
        change_priority.__name__ = key
        change_priority.short_description = f'Change specific priority to {label}'
        actions.append(change_priority)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)


