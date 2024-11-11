from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import gdp_populations_views

urlpatterns = [
    # gdp_populationss
    # path('', gdp_populationss_views.index, name='index'),
    re_path(
        r"^gdp_populations/datatable/$",
        gdp_populations_views.AjaxGdpPopulationsListView.as_view(),
        name="gdp_populations_datatable",
    ),
    #index
    re_path(
        r"^gdp_populations/json/$",
        gdp_populations_views.json_gdp_populations,
        name="json_gdp_populations",
    ),
    re_path(
        r"^gdp_populations/index/$", gdp_populations_views.index, name="gdp_populations_index"
    ),
    re_path(
        r"^gdp_populations/index/service-worker.js",
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
        r"^gdp_populations/select-single/$",
        gdp_populations_views.select_single,
        name="gdp_populations_select_single",
    ),
    re_path(
        r"^gdp_populations/select-multiple/$",
        gdp_populations_views.select_multiple,
        name="gdp_populations_select_multiple",
    ),
    # create
    re_path(
        r"^gdp_populations/create/$",
        gdp_populations_views.create,
        name="gdp_populations_create",
    ),
    re_path(
        r"^gdp_populations/create/service-worker.js",
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
        r"^gdp_populations/update/(?P<pk>.+)/$",
        gdp_populations_views.update,
        name="gdp_populations_update",
    ),
    re_path(
        r"^gdp_populations/update/(?P<pk>.+)/service-worker.js",
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
        r"^gdp_populations/view/(?P<pk>.+)/$", gdp_populations_views.view, name="gdp_populations_view"
    ),
    re_path(
        r"^gdp_populations/view/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]
