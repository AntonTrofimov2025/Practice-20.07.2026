from django.contrib.auth.models import User
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.conf import settings


class Statuses(models.TextChoices):
    NEW = 'new', _('New')
    IN_PROGRESS = 'in_progress', _('In progress')
    PENDING = 'pending', _('Pending')
    BLOCKED = 'blocked', _('Blocked')
    DONE = 'done', _('Done')

class Priorities(models.TextChoices):
    LOW = 'l', _('Low')
    MEDIUM = 'm', _('Medium')
    HIGH = 'h', _('High')
    URGENT = 'u', _('Urgent')
    CRITICAL = 'c', _('Critical')


class UniqueID(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4,
                          verbose_name='UUID id')

    class Meta:
        abstract = True

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Project(UniqueID, TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Project's name")
    description = models.TextField(verbose_name='Description')
    files = models.ManyToManyField('ProjectFile', related_name='projects', verbose_name='Files')

    def __str__(self):
        return f'Project: {self.name}'

    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ('-name',)
        # constraints = [models.UniqueConstraint(fields=('name', 'description'),
        #                                        name='unique_name_by_description')]
        unique_together = (('name', 'description'),)




class Task(UniqueID, TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Project's name",
                            validators=[MinLengthValidator(10)])
    description = models.TextField(verbose_name='Description')
    status = models.CharField(max_length=15, choices=Statuses, verbose_name='Status', default=Statuses.NEW)
    priority = models.CharField(max_length=15, choices=Priorities, verbose_name='Priority')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name='Project')
    due_date = models.DateTimeField(blank=True, null=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks', verbose_name='Assignees', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='tasks', verbose_name='Tags')

    def __str__(self):
        return f'Task: {self.name}'

    def __repr__(self):
        return (f'<Task(name={self.name}, description={self.description}, status={self.status},'
                f'priority={self.priority}, due_date={self.due_date}, assignee={self.assignee})>')

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ('due_date', 'assignee')
        unique_together = ('name', 'project')



class Tag(UniqueID, TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'Tag: {self.name}'

    def __repr__(self):
        return f'<Tag(name={self.name})>'



class ProjectFile(UniqueID, TimeStampedModel):
    name = models.CharField(max_length=120, verbose_name='File name')
    file = models.FileField(upload_to='projects/')

    def __str__(self):
        return f'ProjectFile: name {self.name}, path {self.file}'

    class Meta:
        db_table = 'project_files'
        verbose_name = 'ProjectFile'
        verbose_name_plural = 'ProjectFiles'
        ordering = ('-created_at',)

