from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import levels_views

urlpatterns = [
    # levels
    # path('', levels_views.index, name='index'),
    re_path(
        r"^levels/datatable/$",
        levels_views.AjaxLevelsList.as_view(),
        name="levels_datatable",
    ),
    # index
    re_path(
        r"^levels/json/$",
        levels_views.json_levels,
        name="json_levels",
    ),
    re_path(
        r"^levels/index/$", levels_views.index, name="levels_index"
    ),
    re_path(
        r"^levels/index/service-worker.js",
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
        r"^levels/select-single/$",
        levels_views.select_single,
        name="levels_select_single",
    ),
    re_path(
        r"^levels/select-multiple/$",
        levels_views.select_multiple,
        name="levels_select_multiple",
    ),
    # create
    re_path(
        r"^levels/create/$",
        levels_views.create,
        name="levels_create",
    ),
    re_path(
        r"^levels/create/service-worker.js",
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
        r"^levels/update/(?P<pk>.+)/$",
        levels_views.update,
        name="levels_update",
    ),
    re_path(
        r"^levels/update/(?P<pk>.+)/service-worker.js",
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
        r"^levels/view/(?P<pk>.+)/$", levels_views.view, name="levels_view"
    ),
    re_path(
        r"^levels/view/(?P<pk>.+)/service-worker.js",
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
        r"^levels/dropdown/$", levels_views.dropdown, name="dropdown_levels"
    ),
    #type_status_dropdown_levels
    re_path(
        r"^levels/type_status_dropdown/$", levels_views.type_status_dropdown, name="type_status_dropdown_levels" #financing_drop_down
    ),
    # tree
    re_path(
        r"^levels/tree/(?P<pk>.+)/$", levels_views.tree, name="dropdown_tree"
    ),
    # tree edit
    re_path(
        r"^levels/tree-edit/(?P<key>.+)/(?P<model>.+)/(?P<model_id>.+)/$", levels_views.tree_edit, name="dropdown_tree_edit"
    ),
    # tree view
    re_path(
        r"^levels/tree-view/(?P<key>.+)/(?P<model>.+)/(?P<model_id>.+)/$", levels_views.tree_view, name="dropdown_tree_view"
    ),
     # tree edit
    re_path(
        r"^levels/tree-create/(?P<key>.+)/(?P<model>.+)/$", levels_views.tree_create, name="dropdown_tree_create"
    ),
]
