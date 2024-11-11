from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import fundings_views

urlpatterns = [
    re_path(
        r"^fundings/datatable/$",
        fundings_views.AjaxFundingsListView.as_view(),
        name="fundings_datatable_view",
    ),
    # single or multiple select
    re_path(
        r"^fundings/select-single/$",
        fundings_views.select_single,
        name="fundings_select_single",
    ),
    re_path(
        r"^fundings/select-multiple/$",
        fundings_views.select_multiple,
        name="fundings_select_multiple",
    ),
    # create
    re_path(r"^fundings/create/(?P<project_id>.+)/$", fundings_views.create, name="fundings_create"),
    re_path(
        r"^fundings/create/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),

     # update
    re_path(r"^fundings/update/(?P<pk>.+)/$", fundings_views.update, name="fundings_update"),
    re_path(
        r"^fundings/update/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),

     # view
    re_path(r"^fundings/view/(?P<pk>.+)/$", fundings_views.view, name="fundings_view"),
    re_path(
        r"^fundings/view/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]
