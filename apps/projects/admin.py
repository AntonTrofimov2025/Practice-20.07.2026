from django.conf import settings
from django.contrib import admin
from apps.projects.models import Project, Task, Tag, ProjectFile



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'status', 'priority', 'created_at', 'due_date', 'assignee')
    list_filter = ('project', 'status', 'priority', 'created_at', 'due_date', 'assignee')
    search_fields =('name',)



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)


