from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import activities_inputs_views

urlpatterns = [
    # activities_inputs
    # path('', activities_inputs_views.index, name='index'),
    re_path(
        r"^activities_inputs/datatable/$",
        activities_inputs_views.AjaxActivitiesInputsList.as_view(),
        name="activities_inputs_datatable",
    ),
    # single or multiple select
    re_path(
        r"^activities_inputs/select-single/$",
        activities_inputs_views.select_single,
        name="activities_inputs_select_single",
    ),
    re_path(
        r"^activities_inputs/select-multiple/$",
        activities_inputs_views.select_multiple,
        name="activities_inputs_select_multiple",
    ),
    # create
    re_path(r"^activities_inputs/create/(?P<activity_id>.+)/$", activities_inputs_views.create, name="activities_inputs_create"),
    re_path(
        r"^activities_inputs/create/service-worker.js",
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
        r"^activities_inputs/update/(?P<pk>.+)/$",
        activities_inputs_views.update,
        name="activities_inputs_update",
    ),
    re_path(
        r"^activities_inputs/update/(?P<pk>.+)/service-worker.js",
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
        r"^activities_inputs/view/(?P<pk>.+)/$", activities_inputs_views.view, name="activities_inputs_view"
    ),
    re_path(
        r"^activities_inputs/view/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # index
    re_path(
        r"^activities_inputs/json/$", activities_inputs_views.json_activities_inputs, name="json_activities_inputs"
    ),
    re_path(r"^activities_inputs/index/$", activities_inputs_views.index, name="activities_inputs_index"),
    re_path(
        r"^activities_inputs/index/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ), 

    #Add  expenditure
    re_path(
        r"^activities_inputs/add_expenditure/(?P<pk>.+)/$",
        activities_inputs_views.add_expenditure,
        name="activities_inputs_expenditure",
    ),
    re_path(
        r"^activities_inputs/add_expenditure/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]
