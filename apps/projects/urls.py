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

urlpatterns = [
    path('projects/', projects_.get_all_projects),
    path('projects/<uuid:pk>', projects_.get_project_by_id),
    path('tasks/', projects_.get_all_tasks),
    path('tasks/<uuid:pk>', projects_.get_task_by_id),
    path('tasks/<uuid:pk>/info', projects_.get_task_info),
    path('tags/', projects_.post_or_show_all_tags),
    path('tags/<uuid:pk>', projects_.get_or_upd_tag_by_id)
]
