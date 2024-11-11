from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from app import settings
from app.models.implementers import Implementers
from app.models.files import Files
from app.utils import Utils


class ImplementersTableView(tables.Table):
    auth_permissions = {}
    implementer_name = tables.Column(
        verbose_name="Implementer Name",
        attrs={
            "search_filter": "input-text",
        },
    )
    implementer_section = tables.Column(
        verbose_name="Section",
        attrs={
            "search_filter": "input-text",
        },
    )
    implementer_attachment = tables.Column(
        verbose_name="Attachment",
        attrs={
            "search_filter": "input-text",
        },
    )
    implementer_updated_at = tables.Column(
        verbose_name="Updated At",
        attrs={
            "search_filter": "input-date",
        },
    )
    implementer_updated_by = tables.Column(
        verbose_name="Updated By",
        attrs={
            "search_filter": "input-text",
        },
    )

    def __init__(self, *args, **kwargs):
        self.counter = itertools.count(1)
        super(ImplementersTableView, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_implementer_name(record: Implementers):
        return str(record.implementer_name)

    @staticmethod
    def render_implementer_updated_at(record: Implementers):
        return (
            Utils.get_convert_datetime(
                record.implementer_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

    @staticmethod
    def render_implementer_updated_by(record: Implementers):
        return str(record.implementer_updated_by)

    class Meta:
        order_column_index = 1
        order_column_sort = "desc"
        attrs = {
            "id": "table-" + "Implementers",
            "name": "Implementers",
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "implementer_name",
                },
                {
                    "data": "implementer_updated_at",
                },
                {
                    "data": "implementer_updated_by",
                },
            ],
        }
        sequence = (
            "implementer_name",
            "implementer_updated_at",
            "implementer_updated_by",
        )
        fields = (
            "implementer_name",
            "implementer_updated_at",
            "implementer_updated_by",
        )
        template_name = "_include/bootstrap-datatable-server.html"
