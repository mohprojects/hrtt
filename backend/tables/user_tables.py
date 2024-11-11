from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.users import Users
from app.models.organizations import Organizations
# from app.models.divisions import Divisions


class UsersTable(tables.Table):
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
    user_username = tables.Column(
        verbose_name="Email Id",
        attrs={
            "search_filter": "input-text",
        },
    )
    user_name = tables.Column(
        verbose_name="Name",
        attrs={
            "search_filter": "input-text",
        },
    )
    user_contact_phone_number = tables.Column(
        verbose_name="Phone Number",
        attrs={
            "search_filter": "input-text",
        },
    )
    organization_id = tables.Column(
        verbose_name="Organization",
        attrs={
            "search_filter": "input-text",
        },
    )

    user_role = tables.Column(
        verbose_name="Role",
        attrs={
            "search_filter": "input-select",
            "search_data": Users.DROPDOWN_TYPE,
            "search_type": "status",
            "th_style": "width:100px;",
        },
    )
    user_status = tables.Column(
        verbose_name="Status",
        attrs={
            "search_filter": "input-select",
            "search_data": Users.ARRAY_TEXT_STATUS,
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
        super(UsersTable, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = "<a href=" + str(record.pk) + ">" + "%d" % counter + "</a>"
        return value

    @staticmethod
    def render_actions(record, auth_permissions):
        data = ""
        if settings.ACCESS_PERMISSION_USER_VIEW in auth_permissions.values():
            url = reverse("users_view", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-eye"></i></button>&nbsp;'
            )
        if settings.ACCESS_PERMISSION_USER_UPDATE in auth_permissions.values():
            url = reverse("users_update", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-edit"></i></button>&nbsp;'
            )
    
        if settings.ACCESS_PERMISSION_USER_DELETE in auth_permissions.values():
            url = reverse("users_select_single")
            data += (
                '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\''
                + url
                + "', 'delete', '"
                + str(record.user_id)
                + '\');" ><i class="fa fa-trash"></i></button>&nbsp;'
            )

        return data

    @staticmethod
    def render_user_username(record: Users):
        return mark_safe(
            "<a href="
            + reverse("users_view", args=[record.pk])
            + " style='text-decoration:underline; color:#1B82DC;' >"
            + str(record.user_username)
            + "</a>"
        )

    @staticmethod
    def render_user_name(record: Users):
        return record.user_name

    @staticmethod
    def render_user_contact_phone_number(record: Users):
        return record.user_contact_phone_number

    @staticmethod
    def render_user_role(record: Users):
        role= record.user_role.replace("-", " ").title()
        return role

    @staticmethod
    def render_organization_id(record: Users):
        if record.organization_id != 0:
            try:
                item = Organizations.objects.get(pk=record.organization_id)
                return str(item.organization_name)
            except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                return "-"
        return "All"


    @staticmethod
    def render_user_status(record: Users):
        if record.user_status == Users.STATUS_ACTIVE:
            value = Users.HTML_TAG_STATUS_ACTIVE_COLOR
        elif record.user_status == Users.STATUS_BLOCKED:
            value = Users.HTML_TAG_STATUS_BLOCKED_COLOR
        elif record.user_status == Users.STATUS_UNVERIFIED:
            value = Users.HTML_TAG_STATUS_UNVERIFIED_COLOR
        elif record.user_status == Users.STATUS_UNAPPROVED:
            value = Users.HTML_TAG_STATUS_UNAPPROVED_COLOR
        else:
            value = Users.HTML_TAG_STATUS_INACTIVE_COLOR
        return value

    class Meta:
        model = Users
        order_column_index = 1
        order_column_sort = "asc"
        attrs = {
            "id": "table-" + Users.NAME,
            "name": Users.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "row_number",
                },
                {
                    "data": "user_username",
                },
                {
                    "data": "user_name",
                },
                {
                    "data": "user_contact_phone_number",
                },
                {
                    "data": "organization_id",
                },
              
                {
                    "data": "user_role",
                },
                {
                    "data": "user_status",
                },
                {
                    "data": "actions",
                },
            ],
        }
        sequence = (
            "row_number",
            "user_username",
            "user_name",
            "user_contact_phone_number",
            "organization_id",
            "user_role",
            "user_status",
            "actions",
        )
        fields = (
            "user_username",
            "user_name",
            "user_contact_phone_number",
            "organization_id",
            "user_role",
            "user_status",
        )
        template_name = "_include/bootstrap-datatable-server.html"
