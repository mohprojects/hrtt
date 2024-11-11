from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.currency_rates import Currency_Rates
from django.contrib.humanize.templatetags.humanize import intcomma

class CurrencyRatesTable(tables.Table):
    auth_permissions = {}

    row_number = tables.Column(
        verbose_name="Id",
        attrs={
            "search_filter": "",
            "th_style": "width:60px;",
        },
        orderable=False,
        empty_values=(),
        accessor="pk",
    )
    rate_fiscal_year = tables.Column(
        verbose_name="Fiscal Year",
        attrs={
            "search_filter": "input-text",
        },
    )
    rate_currency = tables.Column(
        verbose_name="Rate Currency",
        attrs={
            "search_filter": "input-text",
        },
    )
    rate_rate = tables.Column(
        verbose_name="Rate",
        attrs={
            "search_filter": "input-text",
        },
    )
    
    actions = tables.Column(
        verbose_name="Actions",
        attrs={
            "search_filter": "",
            "th_style": "width:81px;",
        },
        orderable=False,
        empty_values=(),
    )

    def __init__(self, *args, **kwargs):
        self.counter = itertools.count(1)
        super(CurrencyRatesTable, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = "<a href=" + str(record.pk) + ">" + "%d" % counter + "</a>"
        return value

    @staticmethod
    def render_actions(record, auth_permissions):
        data = ""
        if settings.ACCESS_PERMISSION_CURRENCY_RATES_VIEW in auth_permissions.values():
            url = reverse("currency_rates_view", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-eye"></i></button>&nbsp;'
            )
        if settings.ACCESS_PERMISSION_CURRENCY_RATES_UPDATE in auth_permissions.values():
            url = reverse("currency_rates_update", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-edit"></i></button>&nbsp;'
            )
        if settings.ACCESS_PERMISSION_CURRENCY_RATES_DELETE in auth_permissions.values():
            url = reverse("currency_rates_select_single")
            data += (
                '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\''
                + url
                + "', 'delete', '"
                + str(record.pk)
                + '\');" ><i class="fa fa-trash"></i></button>&nbsp;'
            )
        return data

    @staticmethod
    def render_rate_fiscal_year(record: Currency_Rates):
        return mark_safe(
            "<a href="
            + reverse("currency_rates_view", args=[record.pk])
            + " style='text-decoration:underline; color:#1B82DC;' >"
            + str(record.rate_fiscal_year)
            + "</a>"
        )

    @staticmethod
    def render_rate_currency(record: Currency_Rates):
        return str(intcomma(record.rate_currency))

    @staticmethod
    def render_rate_rate(record: Currency_Rates):
        return str(intcomma(record.rate_rate))

    class Meta:
        model = Currency_Rates
        order_column_index = 1
        order_column_sort = "asc"
        attrs = {
            "id": "table-" + Currency_Rates.NAME,
            "name": Currency_Rates.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "row_number",
                },
                {
                    "data": "rate_fiscal_year",
                },
                {
                    "data": "rate_currency",
                },
                {
                    "data": "rate_rate",
                },
           
                {
                    "data": "actions",
                },
            ],
        }
        sequence = (
            "row_number",
            "rate_fiscal_year",
            "rate_currency",
            "rate_rate",
            "actions",
        )
        fields = (
            "rate_fiscal_year",
            "rate_currency",
            "rate_rate",
        )
        template_name = "_include/bootstrap-datatable-server.html"
