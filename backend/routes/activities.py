from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import activities_view

urlpatterns = [
    # activities
    #path('', activities_view.index, name='index'),
    re_path(
        r"^activities/datatable/$",
        activities_view.AjaxActivitiesList.as_view(),
        name="activities_datatable",
    ),
    # single or multiple select
    re_path(
        r"^activities/select-single/$",
        activities_view.select_single,
        name="activities_select_single",
    ),
    re_path(
        r"^activities/select-multiple/$",
        activities_view.select_multiple,
        name="activities_select_multiple",
    ),
    # create
    re_path(r"^activities/create/(?P<project_id>.+)/$", activities_view.create, name="activities_create"),
    re_path(
        r"^activities/create/(?P<project_id>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # update
    re_path(
        r"^activities/update/(?P<pk>.+)/$",
        activities_view.update,
        name="activities_update",
    ),
    re_path(
        r"^activities/update/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # view
    re_path(
        r"^activities/view/(?P<pk>.+)/$", activities_view.view, name="activities_view"
    ),
    re_path(
        r"^activities/view/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # index
    # re_path(
    #     r"^activities/json/$", activities_view.json_activities, name="json_activities"
    # ),
    re_path(r"^activities/index/(?P<project_id>.+)$", activities_view.index, name="activities_index"),
    re_path(
        r"^activities/index/(?P<project_id>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ), 
    
    re_path(r"^activities/table/$", activities_view.table, name="activities_table"),
    re_path(
        r"^activities/table/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]
#update_activity_input_status