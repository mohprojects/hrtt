from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import system_reports_views

urlpatterns = [
    # index
    re_path(r"^system-reports/index/(?P<pk>.+)/$",
            system_reports_views.index, name="system_reports_index"),
    re_path(
        r"^system-reports/index/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    re_path(
        r"^system-reports/gdp/$",
        system_reports_views.get_gdp,
        name="system_reports_get_gdp",
    ),
    re_path(
        r"^system-reports/exchange-rate/$",
        system_reports_views.get_exchange_rate,
        name="system_reports_get_exchange_rate",
    ),
    re_path(
        r"^system-reports/table-1-121/$",
        system_reports_views.get_table_1_121,
        name="system_reports_get_table_1_121",
    ),
    re_path(
        r"^system-reports/table-1-12211/$",
        system_reports_views.get_table_1_12211,
        name="system_reports_get_table_1_12211",
    ),
    # re_path(
    #     r"^system-reports/table-1-12212/$",
    #     system_reports_views.get_table_1_12212,
    #     name="system_reports_get_table_1_12212",
    # ),
    re_path(
        r"^system-reports/table-1-12213/$",
        system_reports_views.get_table_1_12213,
        name="system_reports_get_table_1_12213",
    ),
    re_path(
        r"^system-reports/table-1-12214/$",
        system_reports_views.get_table_1_12214,
        name="system_reports_get_table_1_12214",
    ),
    re_path(
        r"^system-reports/table-1-12221/$",
        system_reports_views.get_table_1_12221,
        name="system_reports_get_table_1_12221",
    ),
    re_path(
        r"^system-reports/table-1-13/$",
        system_reports_views.get_table_1_13,
        name="system_reports_get_table_1_13",
    ),
    re_path(
        r"^system-reports/table-2/$",
        system_reports_views.get_table_2,
        name="system_reports_get_table_2",
    ),
    re_path(
        r"^system-reports/table-3/$",
        system_reports_views.get_table_3,
        name="system_reports_get_table_3",
    ),
    re_path(
        r"^system-reports/table-4/$",
        system_reports_views.get_table_4,
        name="system_reports_get_table_4",
    ),
    re_path(
        r"^system-reports/table-5/$",
        system_reports_views.get_table_5,
        name="system_reports_get_table_5",
    ),
    re_path(
        r"^system-reports/table-6-public/$",
        system_reports_views.get_table_6_public,
        name="system_reports_get_table_6_public",
    ),
    re_path(
        r"^system-reports/table-6-private/$",
        system_reports_views.get_table_6_private,
        name="system_reports_get_table_6_private",
    ),
    re_path(
        r"^system-reports/table-6-external/$",
        system_reports_views.get_table_6_external,
        name="system_reports_get_table_6_external",
    ),
    re_path(
        r"^system-reports/table-9/$",
        system_reports_views.get_table_9,
        name="system_reports_get_table_9",
    ),
]
