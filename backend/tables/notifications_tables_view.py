from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from django.urls import reverse
from app import settings
from app.models.notifications import Notifications
from app.utils import Utils


class NotificationsTableView(tables.Table):
    auth_permissions = {}

    notification_url = tables.Column(
        verbose_name="Url",
        attrs={
            "search_filter": "input-text",
        },
        orderable=False,
    )
    notification_message = tables.Column(
        verbose_name="Message",
        attrs={
            "search_filter": "input-text",
        },
        orderable=False,
    )
    notification_updated_at = tables.Column(
        verbose_name="Updated At",
        attrs={
            "search_filter": "input-date",
            "th_style": "width:10px;",
        },
        orderable=False,
    )
    notification_updated_by = tables.Column(
        verbose_name="Updated By",
        attrs={
            "search_filter": "input-text",
            "th_style": "width:100px;",
        },
        orderable=False,
    )

    def __init__(self, *args, **kwargs):
        self.counter = itertools.count(1)
        super(NotificationsTableView, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    # @staticmethod
    # def render_row_number(record, counter):
    #     return str(record['_id']['$oid'])

    @staticmethod
    def render_notification_url(record: Notifications):
        url = "#"
        if record["model"] == "users":
            url = reverse("users_view", args=[record["modelId"]])
        if record['model'] == 'activities':
            url = reverse("activities_view", args=[record['modelId']])
        if record["model"] == "reports":
            url = reverse("reporters_reports_view", args=[record["modelId"]])
        return str(url)

    @staticmethod
    def render_notification_message(record: Notifications):
        return str(record["message"])

    @staticmethod
    def render_notification_updated_at(record: Notifications):
        return (
            Utils.get_convert_datetime(
                record["updatedAt"],
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

    @staticmethod
    def render_notification_updated_by(record: Notifications):
        return str(record["updatedBy"])

    class Meta:
        order_column_index = 1
        order_column_sort = "desc"
        attrs = {
            "id": "table-" + Notifications.NAME,
            "name": Notifications.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "notification_url",
                },
                {
                    "data": "notification_message",
                },
                {
                    "data": "notification_updated_at",
                },
                {
                    "data": "notification_updated_by",
                },
            ],
        }
        sequence = (
            "notification_url",
            "notification_message",
            "notification_updated_at",
            "notification_updated_by",
        )
        fields = (
            "message",
            "updatedAt",
            "updatedBy",
        )
        template_name = "_include/bootstrap-datatable-server-logs.html"
