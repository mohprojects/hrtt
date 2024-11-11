from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.methods.status import Methods_Status
from app.models.levels import Levels
from app.models.users import Users
from app.utils import Utils


class LevelsTable(tables.Table):
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
    level_code = tables.Column(
        verbose_name="Code",
        attrs={
            "search_filter": "input-text",
        },
    )
    level_name = tables.Column(
        verbose_name="Name",
        attrs={
            "search_filter": "input-text",
        },
    )
    level_parent = tables.Column(
        verbose_name="Parent",
        attrs={
            "search_filter": "input-text",
        },
    )
    level_key = tables.Column(
        verbose_name="Key",
        attrs={
            "search_filter": "input-text",
        },
    )
    # level_updated_at = tables.Column(
    #     verbose_name="Updated At",
    #     attrs={
    #         "search_filter": "input-date",
    #     },
    # )
    # level_updated_by = tables.Column(
    #     verbose_name="Updated By",
    #     attrs={
    #         "search_filter": "input-text",
    #     },
    # )
    # level_status = tables.Column(
    #     verbose_name="Status",
    #     attrs={
    #         "search_filter": "input-select",
    #         "search_data": Methods_Status.ARRAY_TEXT_STATUS,
    #         "search_code": "status",
    #         "th_style": "width:100px;",
    #     },
    # )
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
        super(LevelsTable, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = "<a href=" + str(record.pk) + ">" + "%d" % counter + "</a>"
        return value

    @staticmethod
    def render_actions(record, auth_permissions):
        data = ""
        if settings.ACCESS_PERMISSION_LEVELS_VIEW in auth_permissions.values():
            url = reverse("levels_view", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-eye"></i></button>&nbsp;'
            )
        if settings.ACCESS_PERMISSION_LEVELS_UPDATE in auth_permissions.values():
            url = reverse("levels_update", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-edit"></i></button>&nbsp;'
            )
        if settings.ACCESS_PERMISSION_LEVELS_DELETE in auth_permissions.values():
            url = reverse("levels_select_single")
            data += (
                '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\''
                + url
                + "', 'delete', '"
                + str(record.pk)
                + '\');" ><i class="fa fa-trash"></i></button>&nbsp;'
            )
        return data

    @staticmethod
    def render_level_code(record: Levels):
        return mark_safe(
            "<a href="
            + reverse("levels_view", args=[record.pk])
            + " style='text-decoration:underline; color:#1B82DC;' >"
            + str(record.level_code)
            + "</a>"
        )

    @staticmethod
    def render_level_name(record: Levels):
        return str(record.level_name)

    @staticmethod
    def render_level_parent(record: Levels):
        try:
            level = Levels.objects.get(pk=record.level_parent)
            record.level_parent = mark_safe(
                "<a href="
                + reverse("levels_view", args=[record.level_parent])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(level.level_code) + ': ' +str(level.level_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            record.level_parent = "-"
        return str(record.level_parent)
    
    @staticmethod
    def render_level_key(record: Levels):
        return str(record.level_key)

    # @staticmethod
    # def render_level_updated_at(record: Levels):
    #     return (
    #         Utils.get_convert_datetime(
    #             record.level_updated_at,
    #             settings.TIME_ZONE,
    #             settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
    #         )
    #         + " "
    #         + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
    #     )

    # @staticmethod
    # def render_level_updated_by(record: Levels):
    #     try:
    #         user = Users.objects.get(pk=record.level_updated_by)
    #         return str(user.user_name)
    #     except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
    #         return "-"

    # @staticmethod
    # def render_level_status(record: Levels):
    #     if record.level_status == Methods_Status.STATUS_ACTIVE:
    #         value = Methods_Status.HTML_TAG_STATUS_ACTIVE_COLOR
    #     elif record.level_status == Methods_Status.STATUS_BLOCKED:
    #         value = Methods_Status.HTML_TAG_STATUS_BLOCKED_COLOR
    #     return value

    class Meta:
        model = Levels
        order_column_index = 1
        order_column_sort = "asc"
        attrs = {
            "id": "table-" + Levels.NAME,
            "name": Levels.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "row_number",
                },
                {
                    "data": "level_code",
                },
                {
                    "data": "level_name",
                },
                {
                    "data": "level_parent",
                },
                {
                    "data": "level_key",
                },
                # {
                #     "data": "level_updated_at",
                # },
                # {
                #     "data": "level_updated_by",
                # },
                # {
                #     "data": "level_status",
                # },
                {
                    "data": "actions",
                },
            ],
        }
        sequence = (
            "row_number",
            "level_code",
            "level_name",
            "level_parent",
            "level_key",
            # "level_updated_at",
            # "level_updated_by",
            # "level_status",
            "actions",
        )
        fields = (
            "level_code",
            "level_name",
            "level_parent",
             "level_key",
            # "level_updated_at",
            # "level_updated_by",
            # "level_status",
        )
        template_name = "_include/bootstrap-datatable-server.html"
