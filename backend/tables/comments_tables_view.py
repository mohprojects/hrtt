from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from app import settings
from app.models.comments import Comments
from app.models.files import Files
from app.utils import Utils


class CommentsTableView(tables.Table):
    auth_permissions = {}
    comment_message = tables.Column(
        verbose_name="Message",
        attrs={
            "search_filter": "input-text",
        },
    )
    comment_section = tables.Column(
        verbose_name="Section",
        attrs={
            "search_filter": "input-text",
        },
    )
    # comment_attachment = tables.Column(
    #     verbose_name="Attachment",
    #     attrs={
    #         "search_filter": "input-text",
    #     },
    # )
    comment_updated_at = tables.Column(
        verbose_name="Updated At",
        attrs={
            "search_filter": "input-date",
        },
    )
    comment_updated_by = tables.Column(
        verbose_name="Updated By",
        attrs={
            "search_filter": "input-text",
        },
    )

    def __init__(self, *args, **kwargs):
        self.counter = itertools.count(1)
        super(CommentsTableView, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_comment_message(record: Comments):
        return str(record.comment_message)

    @staticmethod
    def render_comment_section(record: Comments):
        return str(record.comment_section)

    # @staticmethod
    # def render_comment_attachment(record: Comments):
    #     try:
    #         attachment = Files.objects.get(pk=str(record.comment_attachment))
    #         record.comment_attachment = attachment.file_path
    #     except (TypeError, ValueError, OverflowError, Files.DoesNotExist):
    #         record.comment_attachment = None
    #     return record.comment_attachment

    @staticmethod
    def render_comment_updated_at(record: Comments):
        return (
            Utils.get_convert_datetime(
                record.comment_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

    @staticmethod
    def render_comment_updated_by(record: Comments):
        return str(record.comment_updated_by)

    class Meta:
        order_column_index = 1
        order_column_sort = "desc"
        attrs = {
            "id": "table-" + Comments.NAME,
            "name": Comments.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "comment_message",
                },
                {
                    "data": "comment_updated_at",
                },
                {
                    "data": "comment_updated_by",
                },
            ],
        }
        sequence = (
            "comment_message",
            "comment_updated_at",
            "comment_updated_by",
        )
        fields = (
            "comment_message",
            "comment_updated_at",
            "comment_updated_by",
        )
        template_name = "_include/bootstrap-datatable-server-comments.html"
