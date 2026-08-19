from dis import Positions

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from apps.projects.models import UniqueID, TimeStampedModel
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin, UniqueID, TimeStampedModel):

    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    phone = models.CharField(max_length=75, blank=True, default='')
    last_login = models.DateTimeField(null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    @staticmethod
    @receiver(user_logged_in)
    def logged_in(sender, request, user, **kwargs):
        user.last_login = timezone.now()
        user.save()

    class Positions(models.TextChoices):
        CEO = 'ceo', _('CEO')
        CTO = 'cto', _('CTO')
        DESIGNER = 'dsg', _('Designer')
        PROGRAMMER = 'prg', _('Programmer')
        PRODUCT_OWNER = 'prdo', _('Product Owner')
        PROJECT_OWNER = 'pro', _('Project Owner')
        PROJECT_MANAGER = 'prm', _('Project Manager')
        QA = 'qa', _('QA')

    position = models.CharField(choices=Positions, verbose_name='Positions')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
                       "first_name",
                       "last_name",
                       "position"
                      ]

    def __str__(self):
        return self.username

