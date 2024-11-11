from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.methods.status import Methods_Status
from app.models.reports import Reports
from app.models.projects import Projects
from app.models.users import Users
from app.models.levels import Levels
from app.utils import Utils


class ReportsTable(tables.Table):
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

    report_asset_name = tables.Column(
        verbose_name="Asset Name",
        attrs={
            "search_filter": "input-text",
        },
    )
    report_purchase_value = tables.Column(
        verbose_name="Purchase Value",
        attrs={
            "search_filter": "input-text",
        },
    )
    report_year_purchased = tables.Column(
        verbose_name="Year Purchased",
        attrs={
            "search_filter": "input-text",
        },
    )
    report_updated_at = tables.Column(
        verbose_name="Updated At",
        attrs={
            "search_filter": "input-date",
        },
    )
    report_updated_by = tables.Column(
        verbose_name="Updated By",
        attrs={
            "search_filter": "input-text",
        },
    )

    report_status = tables.Column(
        verbose_name="Status",
        attrs={
            "search_filter": "input-select",
            "search_data": Reports.ARRAY_TEXT_STATUS,
            "search_type": "status",
            "th_style": "width:100px;",
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
        super(ReportsTable, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = "<a href=" + str(record.pk) + ">" + "%d" % counter + "</a>"
        return value

    @staticmethod
    def render_actions(record, auth_permissions):
        data = ""
        if settings.ACCESS_PERMISSION_ACTIVITIES_VIEW in auth_permissions.values():
            url1 = reverse("reports_view",args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \''
                + url1
                + '\';"><i class="fa fa-eye"></i></button>&nbsp;'
            )
        if record.report_status== record.STATUS_DRAFT or record.report_status == record.STATUS_REJECTED :
            if settings.ACCESS_PERMISSION_ACTIVITIES_UPDATE in auth_permissions.values():
                url2 = reverse("reports_update",args=[record.pk])
                data += (
                    '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \''
                    + url2
                    + '\';"><i class="fa fa-edit"></i></button>&nbsp;'
                )
            if settings.ACCESS_PERMISSION_ACTIVITIES_DELETE in auth_permissions.values():
                url3 = reverse("reports_select_single")
                data += (
                    '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\''
                    + url3
                    + "', 'delete', '"
                    + str(record.pk)
                    + '\');" ><i class="fa fa-trash"></i></button>&nbsp;'
                )
        return data

    @staticmethod
    def render_report_asset_name(record: Reports):
        return mark_safe(
            "<a href="
            + reverse("reports_view",args=[record.pk])
            + " style='text-decoration:underline; color:#1B82DC;' >"
            + str(record.report_asset_name)
            + "</a>"
        )


    @staticmethod
    def render_report_purchase_value(record: Reports):
        purchase = record.report_purchase_value
        currency = record.report_purchase_currency
        return Utils.format_amount_with_commas(purchase) + " "+ currency
    
    @staticmethod
    def render_report_year_purchased(record: Reports):
        return str(record.report_year_purchased)

    @staticmethod
    def render_report_updated_at(record: Reports):
        return (
            Utils.get_convert_datetime(
                record.report_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

    @staticmethod
    def render_report_updated_at(record: Reports):
        return (
            Utils.get_convert_datetime(
                record.report_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

    @staticmethod
    def render_report_updated_by(record: Reports):
        try:
            user = Users.objects.get(pk=record.report_updated_by)
            return str(user.user_name)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            return "-"

    @staticmethod
    def render_report_status(record: Reports):
        if record.report_status == Methods_Status.STATUS_DRAFT:
            value = Methods_Status.HTML_TAG_STATUS_DRAFT_COLOR
            return value
        if record.report_status == Methods_Status.STATUS_SUBMITTED:
            value = Methods_Status.HTML_TAG_STATUS_SUBMITTED_COLOR
            return value
        if record.report_status == Methods_Status.STATUS_ACCEPTED:
            value = Methods_Status.HTML_TAG_STATUS_ACCEPTED_COLOR
            return value
        if record.report_status == Methods_Status.STATUS_REJECTED:
            value = Methods_Status.HTML_TAG_STATUS_REJECTED_COLOR
            return value
        if record.report_status == Reports.STATUS_APPROVED:
            value = Reports.HTML_TAG_STATUS_APPROVED_COLOR
            return value
        if record.report_status == Reports.STATUS_DENIED:
            value = Reports.HTML_TAG_STATUS_DENIED_COLOR
            return value

    class Meta:
        model = Reports

        order_column_index = 1
        order_column_sort = "asc"
        attrs = {
            "id": "table-" + Reports.NAME,
            "name": Reports.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "row_number",
                },
                {
                    "data": "report_asset_name",
                },
                # {
                #     "data": "project_id",
                # },
                {
                    "data": "report_purchase_value",
                },
                {
                    "data": "report_year_purchased",
                },
                {
                    "data": "report_updated_at",
                },
                {
                    "data": "report_updated_by",
                },
                {
                    "data": "report_status",
                },
                {
                    "data": "actions",
                },
            ],
        }
        sequence = (
            "row_number",
            "report_asset_name",
            #"project_id",
            "report_purchase_value",
            "report_year_purchased",
            "report_updated_at",
            "report_updated_by",
            "report_status",
            "actions",
        )
        fields = (
            "report_asset_name",
            #"project_id",
            "report_purchase_value",
            "report_year_purchased",
            "report_updated_at",
            "report_updated_by",
            "report_status",
        )
        template_name = "_include/bootstrap-datatable-server.html"
        #template_name = "_include/bootstrap-datatable-server-divisions.html"
