from django.urls import path
from .generic_views import UserListGenericView, DownloadProjectFileView


urlpatterns = [
    path('users/', UserListGenericView.as_view(), name='user-list-view'),
    path('files/download/<uuid:pk>', DownloadProjectFileView.as_view(), name='file-retrieve-view')
]

