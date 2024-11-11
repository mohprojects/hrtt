from django.urls import path, re_path
from django.views.generic import TemplateView

from backend.views import projects_views

urlpatterns = [
    # projects
    path("", projects_views.index, name="index"),
    re_path(
        r"^projects/datatable/$",
        projects_views.AjaxProjectsList.as_view(),
        name="projects_datatable",
    ),
    # index
    re_path(r"^projects/json/$", projects_views.json_projects,
            name="json_projects"),
    re_path(r"^projects/index/$", projects_views.index, name="projects_index"),
    re_path(
        r"^projects/index/service-worker.js",
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
        r"^projects/select-single/$",
        projects_views.select_single,
        name="projects_select_single",
    ),
    re_path(
        r"^projects/select-multiple/$",
        projects_views.select_multiple,
        name="projects_select_multiple",
    ),
    # create
    re_path(r"^projects/create/$", projects_views.create,
            name="projects_create"),
    re_path(
        r"^projects/create/service-worker.js",
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
        r"^projects/update/(?P<pk>.+)/$", projects_views.update, name="projects_update"
    ),
    re_path(
        r"^projects/update/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # view
    re_path(r"^projects/view/(?P<pk>.+)/$",
            projects_views.view, name="projects_view"),
    re_path(
        r"^projects/view/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),

    re_path(r"^projects/financing_agents/$",
            projects_views.get_financing_agents, name="get_financing_agents"),
    re_path(
        r"^implementers/fetch/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]
