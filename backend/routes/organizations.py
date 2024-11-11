from django.urls import path, re_path
from django.views.generic import TemplateView

from backend.views import organizations_views

urlpatterns = [
    # organizations
    path("", organizations_views.index, name="index"),
    re_path(
        r"^organizations/datatable/$",
        organizations_views.AjaxOrganizationsList.as_view(),
        name="organizations_datatable",
    ),
    # index
    re_path(
        r"^organizations/json/$",
        organizations_views.json_organizations,
        name="json_organizations",
    ),
    re_path(
        r"^organizations/index/$", organizations_views.index, name="organizations_index"
    ),
    re_path(
        r"^organizations/index/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # single or multiple select
    re_path(
        r"^organizations/select-single/$",
        organizations_views.select_single,
        name="organizations_select_single",
    ),
    re_path(
        r"^organizations/select-multiple/$",
        organizations_views.select_multiple,
        name="organizations_select_multiple",
    ),
    # create
    re_path(
        r"^organizations/create/$",
        organizations_views.create,
        name="organizations_create",
    ),
    re_path(
        r"^organizations/create/service-worker.js",
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
        r"^organizations/update/(?P<pk>.+)/$",
        organizations_views.update,
        name="organizations_update",
    ),
    re_path(
        r"^organizations/update/(?P<pk>.+)/service-worker.js",
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
        r"^organizations/view/(?P<pk>.+)/$",
        organizations_views.view,
        name="organizations_view",
    ),
    re_path(
        r"^organizations/view/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # dropdown
    re_path(
        r"^organizations/dropdown/$",
        organizations_views.dropdown,
        name="dropdown_organizations",
    ),
    # update levels type
    re_path(
        r"^organizations/update-levels-type/(?P<pk>.+)/$",
        organizations_views.update_levels_type,
        name="organizations_update_levels_type",
    ),
    re_path(
        r"^organizations/update-levels-status/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    re_path(
        r"^organizations/update-levels-tyoe-submit/(?P<pk>.+)/$",
        organizations_views.update_levels_type_submit,
        name="organizations_update_levels_type_submit",
    ),
    # update levels status
    re_path(
        r"^organizations/update-levels-status/(?P<pk>.+)/$",
        organizations_views.update_levels_status,
        name="organizations_update_levels_status",
    ),
    re_path(
        r"^organizations/update-levels-status/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    re_path(
        r"^organizations/update-levels-status-submit/(?P<pk>.+)/$",
        organizations_views.update_levels_status_submit,
        name="organizations_update_levels_status_submit",
    ),
    # dropdown
    # re_path(
    #     r"^organizations/status_classes/(?P<classification_id>.+)/$",
    #     organizations_views.get_status_classes,
    #     name="organizations_classes",
    # ),
    # re_path(
    #     r"^organizations/status_sub_classes/$",
    #     organizations_views.get_status_sub_classes,
    #     name="organizations_sub_classes",
    # ),
]
