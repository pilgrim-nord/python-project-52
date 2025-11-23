from django.urls import path

from .views import (
    StatusListView,
)

app_name = "statuses"

urlpatterns = [
    path(
        "",
        StatusListView.as_view(),
        name="list"
    ),
]