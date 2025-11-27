"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from task_manager.views import IndexView, CustomLogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.users.urls', namespace='users')),
    path('tasks/', include('task_manager.tasks.urls', namespace='tasks')),
    path('labels/', include('task_manager.labels.urls', namespace='labels')),
    path('statuses/', include('task_manager.statuses.urls', namespace='statuses')),
    # path("logout/", CustomLogoutView.as_view(), name="logout"),
    path('login/', RedirectView.as_view(url=reverse_lazy('users:login'), permanent=True)),
    path('logout/', RedirectView.as_view(url=reverse_lazy('users:logout'), permanent=True)),
]
