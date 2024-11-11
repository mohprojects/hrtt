from django.urls import re_path

from backend.views import logs_views

urlpatterns = [
    # logs
    re_path(
        r"^logs/datatable/view/$",
        logs_views.AjaxLogsListView.as_view(),
        name="logs_datatable_view",
    ),
]
