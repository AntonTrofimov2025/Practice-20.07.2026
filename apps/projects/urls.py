"""
URL configuration for config projects.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views as projects_
from .api_views import TaskDetailAPIView
from apps.projects.api_views import (TagListCreateApiView, TagDetailApiView,
                                     ProjectListApiView, ProjectDetailApiView,
                                     ProjectFileListAPIView)

urlpatterns = [
    path('projects/', ProjectListApiView.as_view(), name='project-list-view'),
    path('projects/<uuid:pk>', ProjectDetailApiView.as_view(), name='project-detail-view'),
    path('tasks/', projects_.get_all_tasks, name='task-list-view'),
    path('tasks_by_name/', projects_.post_task_by_name, name='task-by-name'),
    # path('tasks/<uuid:pk>', projects_.get_task_by_id),
    path('tasks/<uuid:pk>', TaskDetailAPIView.as_view(), name='task-detail-view'),
    path('tasks/<uuid:pk>/info', projects_.get_task_info),
    # path('tags/', projects_.post_or_show_all_tags),
    # path('tags/<uuid:pk>', projects_.get_or_upd_tag_by_id),
    path('tags/', TagListCreateApiView.as_view(), name='tag-list-view'),
    path('tags/<uuid:pk>', TagDetailApiView.as_view(), name='tag-detail-view'),
    path('files/', ProjectFileListAPIView.as_view(), name='file-list-view'),
    path('files/<uuid:pk>', ProjectDetailApiView.as_view(), name='file-detail-view')
]
