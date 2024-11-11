from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.gdp_populations import Gdp_Populations
from django.contrib.humanize.templatetags.humanize import intcomma


class GdpPopulationsTable(tables.Table):
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
    fiscal_year = tables.Column(
        verbose_name="Fiscal Year",
        attrs={
            "search_filter": "input-text",
        },
    )
    population = tables.Column(
        verbose_name="Total Population",
        attrs={
            "search_filter": "input-text",
        },
    )
    budget = tables.Column(
        verbose_name="Total Government Budget",
        attrs={
            "search_filter": "input-text",
        },
    )
    expenditure = tables.Column(
        verbose_name="Total Government Expenditure",
        attrs={
            "search_filter": "input-text",
        },
    )
    gdp = tables.Column(
        verbose_name="GDP",
        attrs={
            "search_filter": "input-text",
        },
    )
    payment_rate = tables.Column(
        verbose_name="OOP(co-payment)",
        attrs={
            "search_filter": "input-text",
        },
    )
    budget_health = tables.Column(
        verbose_name="Government Budget on health",
        attrs={
            "search_filter": "input-text",
        },
    )
    expenditure_health = tables.Column(
        verbose_name="Government Expenditure health",
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
        super(GdpPopulationsTable, self).__init__(*args, **kwargs)

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
            url = reverse("gdp_populations_view", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-eye"></i></button>&nbsp;'
            )
        if settings.ACCESS_PERMISSION_CURRENCY_RATES_UPDATE in auth_permissions.values():
            url = reverse("gdp_populations_update", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-edit"></i></button>&nbsp;'
            )
        if settings.ACCESS_PERMISSION_CURRENCY_RATES_DELETE in auth_permissions.values():
            url = reverse("gdp_populations_select_single")
            data += (
                '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\''
                + url
                + "', 'delete', '"
                + str(record.pk)
                + '\');" ><i class="fa fa-trash"></i></button>&nbsp;'
            )
        return data

    @staticmethod
    def render_fiscal_year(record: Gdp_Populations):
        return mark_safe(
            "<a href="
            + reverse("gdp_populations_view", args=[record.pk])
            + " style='text-decoration:underline; color:#1B82DC;' >"
            + str(record.fiscal_year)
            + "</a>"
        )

    @staticmethod
    def render_population(record: Gdp_Populations):
        return intcomma(record.population)
    
    @staticmethod
    def render_budget(record: Gdp_Populations):
        return intcomma(record.budget)

    @staticmethod
    def render_expenditure(record: Gdp_Populations):
        return intcomma(record.expenditure)
    
    @staticmethod
    def render_gdp(record: Gdp_Populations):
        return intcomma(record.gdp)
    
    @staticmethod
    def render_payment_rate(record: Gdp_Populations):
        return intcomma(record.payment_rate) + ' %'
    
    @staticmethod
    def render_budget_health(record: Gdp_Populations):
        return intcomma(record.budget_health)

    @staticmethod
    def render_expenditure_health(record: Gdp_Populations):
        return intcomma(record.expenditure_health)

    class Meta:
        model = Gdp_Populations
        order_column_index = 1
        order_column_sort = "asc"
        attrs = {
            "id": "table-" + Gdp_Populations.NAME,
            "name": Gdp_Populations.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "row_number",
                },
                {
                    "data": "fiscal_year",
                },
                {
                    "data": "population",
                },
                {
                    "data": "budget",
                },
                {
                    "data": "expenditure",
                },
                {
                    "data": "gdp",
                },
                {
                    "data": "payment_rate",
                },
                {
                    "data": "budget_health",
                },
                {
                    "data": "expenditure_health",
                },
           
                {
                    "data": "actions",
                },
            ],
        }
        sequence = (
            "row_number",
            "fiscal_year",
            "population",
            "budget",
            "expenditure",
            "gdp",
            "payment_rate",
            "budget_health",
            "expenditure_health",
            "actions",
        )
        fields = (
            "fiscal_year",
            "population",
            "budget",
            "expenditure",
            "gdp",
            "payment_rate",
            "budget_health",
            "expenditure_health",
        )
        template_name = "_include/bootstrap-datatable-server.html"
