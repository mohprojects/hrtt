from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import reports_views

urlpatterns = [
    # reports
    # path('', activities_view.index, name='index'),
    # re_path(r"^reports/datatable/$",reports_views.AjaxReportsList.as_view(),name="reports_datatable",),
    # single or multiple select
    re_path(r"^reports/select-single/$",reports_views.select_single,name="reports_select_single",),
    re_path(r"^reports/select-multiple/$",reports_views.select_multiple,name="reports_select_multiple",),
    # create
    re_path(r"^reports/create/(?P<project_id>.+)/$", reports_views.create, name="reports_create"),
    re_path(r"^reports/create/(?P<project_id>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # update
    re_path(r"^reports/update/(?P<pk>.+)/$",reports_views.update,name="reports_update",),
    re_path(r"^reports/update/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # view
    re_path(r"^reports/view/(?P<pk>.+)/$", reports_views.view, name="reports_view"),
    re_path(r"^reports/view/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # index
    re_path(r"^reports/json/$", reports_views.json_reports, name="json_reports"
    ),
    re_path(r"^reports/index/(?P<project_id>.+)$", reports_views.index, name="reports_index"),
    re_path(r"^reports/index/(?P<project_id>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ), 
]
