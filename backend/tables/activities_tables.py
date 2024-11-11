from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.methods.status import Methods_Status
from app.models.activities import Activities
from app.models.projects import Projects
from app.models.users import Users
from app.models.levels import Levels
from app.utils import Utils


class ActivitiesTable(tables.Table):
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
    project_id = tables.Column(
        verbose_name="Project",
        attrs={
            "search_filter": "input-text",
        },
    )

    fiscal_year = tables.Column(
        verbose_name="Fiscal Year",
        attrs={
            "search_filter": "input-text",
        },
    )

    activity_name = tables.Column(
        verbose_name="Name",
        attrs={
            "search_filter": "input-text",
        },
    )
    activity_location = tables.Column(
        verbose_name="Location ",
        attrs={
            "search_filter": "input-text",
        },
    )
 
    activity_updated_at = tables.Column(
        verbose_name="Updated At",
        attrs={
            "search_filter": "input-date",
        },
    )
    activity_updated_by = tables.Column(
        verbose_name="Updated By",
        attrs={
            "search_filter": "input-text",
        },
    )
    activity_status = tables.Column(
        verbose_name="Status",
        attrs={
            "search_filter": "input-select",
            "search_data": Activities.ARRAY_TEXT_STATUS,
            "search_description": "status",
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
        super(ActivitiesTable, self).__init__(*args, **kwargs)

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
            url = reverse("activities_view", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-eye"></i></button>&nbsp;'
            )

        if (record.activity_status == record.STATUS_DRAFT or record.activity_status == record.STATUS_BUDGET_REJECTED or 
            record.activity_status == record.STATUS_EXPENSES_REJECTED):
            if settings.ACCESS_PERMISSION_ACTIVITIES_UPDATE in auth_permissions.values():
                url = reverse("activities_update", args=[record.pk])
                data += (
                    '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \''
                    + url
                    + '\';"><i class="fa fa-edit"></i></button>&nbsp;'
                )
            if settings.ACCESS_PERMISSION_ACTIVITIES_DELETE in auth_permissions.values():
                url = reverse("activities_select_single")
                data += (
                    '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\''
                    + url
                    + "', 'delete', '"
                    + str(record.pk)
                    + '\');" ><i class="fa fa-trash"></i></button>&nbsp;'
                )
        return data

    @staticmethod
    def render_activity_name(record: Activities):
        return mark_safe(
            "<a href="
            + reverse("activities_view", args=[record.pk])
            + " style='text-decoration:underline; color:#1B82DC;' >"
            + str(record.activity_name)
            + "</a>"
        )
        
    @staticmethod
    def render_activity_project(record: Activities):
        if record.project_id != 0:
            try:
                item = Projects.objects.get(pk=record.project_id)
                return str(item.project_name)
            except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
                return "-"


    @staticmethod
    def render_activity_fy(record: Activities):
        return record.activity_fiscal_year

    @staticmethod
    def render_activity_location(record: Activities):
        if record.activity_location != 0:
            try:
                item = Levels.objects.get(pk=record.activity_location)
                return str(item.level_name)
            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                return "-"
        
    @staticmethod
    def render_activity_updated_at(record: Activities):
        return (
            Utils.get_convert_datetime(
                record.activity_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

    @staticmethod
    def render_activity_updated_at(record: Activities):
        return (
            Utils.get_convert_datetime(
                record.activity_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

    @staticmethod
    def render_activity_updated_by(record: Activities):
        try:
            user = Users.objects.get(pk=record.activity_updated_by)
            return str(user.user_name)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            return "-"

    @staticmethod
    def render_activity_status(record: Activities):
        if record.activity_status == Activities.STATUS_DRAFT:
            value = Activities.HTML_TAG_STATUS_DRAFT_COLOR
            return value
        if record.activity_status == Activities.STATUS_SUBMITTED:
            value = Activities.HTML_TAG_STATUS_SUBMITTED_COLOR
            return value
        if record.activity_status == Activities.STATUS_BUDGET_ACCEPTED:
            value = Activities.HTML_TAG_STATUS_BUDGET_ACCEPTED_COLOR
            return value
        if record.activity_status == Activities.STATUS_BUDGET_REJECTED:
            value = Activities.HTML_TAG_STATUS_BUDGET_REJECTED_COLOR
            return value
        if record.activity_status == Activities.STATUS_BUDGET_APPROVED:
            value =Activities.HTML_TAG_STATUS_BUDGET_APPROVED_COLOR
            return value
        if record.activity_status == Activities.STATUS_BUDGET_DENIED:
            value =Activities.HTML_TAG_STATUS_BUDGET_DENIED_COLOR
            return value
        if record.activity_status == Activities.STATUS_EXPENSES_ACCEPTED:
            value = Activities.HTML_TAG_STATUS_EXPENSES_ACCEPTED_COLOR
            return value
        if record.activity_status == Activities.STATUS_EXPENSES_REJECTED:
            value = Activities.HTML_TAG_STATUS_EXPENSES_REJECTED_COLOR
            return value
        if record.activity_status == Activities.STATUS_EXPENSES_APPROVED:
            value = Activities.HTML_TAG_STATUS_EXPENSES_APPROVED_COLOR
            return value
        if record.activity_status == Activities.STATUS_EXPENSES_DENIED:
            value = Activities.HTML_TAG_STATUS_EXPENSES_DENIED_COLOR
            return value

    class Meta:
        model = Activities

        order_column_index = 1
        order_column_sort = "asc"
        attrs = {
            "id": "table-" + Activities.NAME,
            "name": Activities.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "row_number",
                },
                {
                    "data": "activity_name",
                },
                {
                    "data": "project_id",
                },
                {
                    "data": "activity_location",
                },
                {
                    "data": "fiscal_year",
                },
                {
                    "data": "activity_updated_at",
                },
                {
                    "data": "activity_updated_by",
                },
                {
                    "data": "activity_status",
                },
                {
                    "data": "actions",
                },
            ],
        }
        sequence = (
            "row_number",
            "activity_name",
            "project_id",
            "activity_location",
            "fiscal_year",
            "activity_updated_at",
            "activity_updated_by",
            "activity_status",
            "actions",
        )
        fields = (
            "activity_name",
            "project_id",
            "fiscal_year",
            "activity_location",
            "activity_updated_at",
            "activity_updated_by",
            "activity_status",
        )
      
        #template_name = "_include/bootstrap-datatable-server-activities.html"
        template_name = "_include/bootstrap-datatable-server.html"
