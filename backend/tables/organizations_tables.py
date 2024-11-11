from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.organizations import Organizations
from app.models.users import Users
from app.models.levels import Levels
from app.utils import Utils


class OrganizationsTable(tables.Table):
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
    organization_name = tables.Column(
        verbose_name="Name",
        attrs={
            "search_filter": "input-text",
        },
    )
    organization_type = tables.Column(
        verbose_name="Type",
        attrs={
            "search_filter": "input-text",
        },
    )
    organization_category = tables.Column(
        verbose_name="Organization  Category",
        attrs={
            "search_filter": "input-text",
        },
    )
    organization_updated_at = tables.Column(
        verbose_name="Updated At",
        attrs={
            "search_filter": "input-date",
        },
    )
    organization_updated_by = tables.Column(
        verbose_name="Updated By",
        attrs={
            "search_filter": "input-text",
        },
    )
    organization_status = tables.Column(
        verbose_name="Status",
        attrs={
            "search_filter": "input-select",
            "search_data": Organizations.ARRAY_TEXT_STATUS,
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
        super(OrganizationsTable, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = "<a href=" + str(record.pk) + ">" + "%d" % counter + "</a>"
        return value

    @staticmethod
    def render_actions(record, auth_permissions):
        data = ""
        if settings.ACCESS_PERMISSION_ORGANIZATIONS_VIEW in auth_permissions.values():
            url = reverse("organizations_view", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-eye"></i></button>&nbsp;'
            )
        if settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE in auth_permissions.values():
            url = reverse("organizations_update", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-edit"></i></button>&nbsp;'
            )
        if settings.ACCESS_PERMISSION_ORGANIZATIONS_DELETE in auth_permissions.values():
            url = reverse("organizations_select_single")
            data += (
                '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\''
                + url
                + "', 'delete', '"
                + str(record.pk)
                + '\');" ><i class="fa fa-trash"></i></button>&nbsp;'
            )
        return data

    @staticmethod
    def render_organization_name(record: Organizations):
        return mark_safe(
            "<a href="
            + reverse("organizations_view", args=[record.pk])
            + " style='text-decoration:underline; color:#1B82DC;' >"
            + str(record.organization_name)
            + "</a>"
        )

    @staticmethod
    def render_organization_type(record: Organizations):
        
        if record.organization_type:
            try:
                type= Levels.objects.get(
                        pk=record.organization_type)
                return mark_safe(str(type.level_name))
            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                print('')
            
        return ""

    @staticmethod
    def render_organization_category(record: Organizations):
        ans = record.organization_category
        resp = "<div class='center-block' style='text-left: center;list-style: square;' >"
        if ans:
            res = ""
            ans = ans.strip('][').split(',')
            for status in ans:
                if status:
                    res = res + "<span class='badge badge-light'>"+ ' '.join(str(e) for e in status.strip(' ').strip("'").split('_')) + "</span>"
            resp = resp + res + "</div>"
            return resp
        return ""


    @staticmethod
    def render_organization_updated_at(record: Organizations):
        return (
            Utils.get_convert_datetime(
                record.organization_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

    @staticmethod
    def render_organization_updated_by(record: Organizations):
        try:
            user = Users.objects.get(pk=record.organization_updated_by)
            return str(user.user_name)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            return "-"

    @staticmethod
    def render_organization_status(record: Organizations):
        if record.organization_status == record.STATUS_ACTIVE:
            value = record.HTML_TAG_STATUS_ACTIVE_COLOR
        elif record.organization_status == record.STATUS_INNACTIVE:
            value = record.HTML_TAG_STATUS_INNACTIVE_COLOR
        return value

    class Meta:
        model = Organizations
        order_column_index = 1
        order_column_sort = "asc"
        attrs = {
            "id": "table-" + Organizations.NAME,
            "name": Organizations.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "row_number",
                },
                {
                    "data": "organization_name",
                },
                {
                    "data": "organization_type",
                },
                {
                    "data": "organization_category",
                },
                {
                    "data": "organization_updated_at",
                },
                {
                    "data": "organization_updated_by",
                },
                {
                    "data": "organization_status",
                },
                {
                    "data": "actions",
                },
            ],
        }
        sequence = (
            "row_number",
            "organization_name",
            "organization_type",
            "organization_category",
            "organization_updated_at",
            "organization_updated_by",
            "organization_status",
            "actions",
        )
        fields = (
            "organization_name",
            "organization_type",
            "organization_category",
            "organization_updated_at",
            "organization_updated_by",
            "organization_status",
        )
        template_name = "_include/bootstrap-datatable-server.html"
