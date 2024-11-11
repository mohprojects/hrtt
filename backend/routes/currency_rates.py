from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import currency_rates_views

urlpatterns = [
    # currency_ratess
    # path('', currency_ratess_views.index, name='index'),
    re_path(
        r"^currency_rates/datatable/$",
        currency_rates_views.AjaxCurrencyRatesListView.as_view(),
        name="currency_rates_datatable",
    ),
    #index
    re_path(
        r"^currency_rates/json/$",
        currency_rates_views.json_currency_rates,
        name="json_currency_rates",
    ),
    re_path(
        r"^currency_rates/index/$", currency_rates_views.index, name="currency_rates_index"
    ),
    re_path(
        r"^currency_rates/index/service-worker.js",
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
        r"^currency_rates/select-single/$",
        currency_rates_views.select_single,
        name="currency_rates_select_single",
    ),
    re_path(
        r"^currency_rates/select-multiple/$",
        currency_rates_views.select_multiple,
        name="currency_rates_select_multiple",
    ),
    # create
    re_path(
        r"^currency_rates/create/$",
        currency_rates_views.create,
        name="currency_rates_create",
    ),
    re_path(
        r"^currency_rates/create/service-worker.js",
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
        r"^currency_rates/update/(?P<pk>.+)/$",
        currency_rates_views.update,
        name="currency_rates_update",
    ),
    re_path(
        r"^currency_rates/update/(?P<pk>.+)/service-worker.js",
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
        r"^currency_rates/view/(?P<pk>.+)/$", currency_rates_views.view, name="currency_rates_view"
    ),
    re_path(
        r"^currency_rates/view/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]
