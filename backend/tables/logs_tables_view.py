from __future__ import unicode_literals

import itertools

import django_tables2 as tables

from app import settings
from app.models.logs import Logs
from app.utils import Utils


class LogsTableView(tables.Table):
    auth_permissions = {}

    # row_number = tables.Column(
    #     verbose_name='Id',
    #     attrs={
    #         'search_filter': '',
    #         'th_style': 'width:10px;',
    #     },
    #     orderable=False,
    #     empty_values=(),
    #     accessor='pk',
    # )
    log_message = tables.Column(
        verbose_name="Message",
        attrs={
            "search_filter": "input-text",
        },
        orderable=False,
    )
    log_updated_at = tables.Column(
        verbose_name="Updated At",
        attrs={
            "search_filter": "input-date",
            "th_style": "width:10px;",
        },
        orderable=False,
    )
    log_updated_by = tables.Column(
        verbose_name="Updated By",
        attrs={
            "search_filter": "input-text",
            "th_style": "width:100px;",
        },
        orderable=False,
    )

    def __init__(self, *args, **kwargs):
        self.counter = itertools.count(1)
        super(LogsTableView, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    # @staticmethod
    # def render_row_number(record, counter):
    #     return str(record['_id']['$oid'])

    @staticmethod
    def render_log_message(record: Logs):
        return str(record["message"])

    @staticmethod
    def render_log_updated_at(record: Logs):
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
    def render_log_updated_by(record: Logs):
        return str(record["updatedBy"])

    class Meta:
        order_column_index = 1
        order_column_sort = "desc"
        attrs = {
            "id": "table-" + Logs.NAME,
            "name": Logs.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "log_message",
                },
                {
                    "data": "log_updated_at",
                },
                {
                    "data": "log_updated_by",
                },
            ],
        }
        sequence = (
            "log_message",
            "log_updated_at",
            "log_updated_by",
        )
        fields = (
            "message",
            "updatedAt",
            "updatedBy",
        )
        template_name = "_include/bootstrap-datatable-server-logs.html"
