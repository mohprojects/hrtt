from django.urls import re_path

from backend.views import notifications_views
from django.views.generic import TemplateView

urlpatterns = [
    # notifications
    re_path(
        r"^notifications/datatable/view/$",
        notifications_views.AjaxNotificationsListView.as_view(),
        name="notifications_datatable_view",
    ),

     # create
    re_path(r"^notifications/create/(?P<project_id>.+)/$", notifications_views.create, name="notifications_create"),
    re_path(
        r"^notifications/create/(?P<project_id>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]
