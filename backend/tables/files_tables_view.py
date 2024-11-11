from __future__ import unicode_literals

import datetime
import itertools

import django_tables2 as tables
import pytz
from app import settings
from app.models.files import Files
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.template.defaultfilters import filesizeformat


class FilesTableView(tables.Table):
    auth_permissions = {}

    # row_number = tables.Column(
    #     verbose_name='Id',
    #     attrs={
    #         'search_filter': '',
    #         'th_style': 'width:60px;',
    #     },
    #     orderable=False,
    #     empty_values=(),
    #     accessor='pk',
    # )
    file_model_no = tables.Column(
        verbose_name="Type",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_name = tables.Column(
        verbose_name="Name",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_size = tables.Column(
        verbose_name="Size",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_type = tables.Column(
        verbose_name="Type",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_mime = tables.Column(
        verbose_name="Mime",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_path = tables.Column(
        verbose_name="Path",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_name_ext = tables.Column(
        verbose_name="Name Ext",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_parent_id = tables.Column(
        verbose_name="Parent Id",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_directory_code = tables.Column(
        verbose_name="Directory Code",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_directory_name = tables.Column(
        verbose_name="Directory Name",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_office_name = tables.Column(
        verbose_name="Office File Name",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_office_type = tables.Column(
        verbose_name="Office File Type",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_office_directory_code = tables.Column(
        verbose_name="Office Directory Code",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_office_directory_name = tables.Column(
        verbose_name="Office Directory Name",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_office_uploaded = tables.Column(
        verbose_name="Office Uploaded",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_updated_at = tables.Column(
        verbose_name="Updated At",
        attrs={
            "search_filter": "input-date",
        },
    )
    file_updated_by = tables.Column(
        verbose_name="Updated By",
        attrs={
            "search_filter": "input-text",
        },
    )
    file_status = tables.Column(
        verbose_name="Status",
        attrs={
            "search_filter": "input-text",
        },
    )

    def __init__(self, *args, **kwargs):
        self.counter = itertools.count(1)
        super(FilesTableView, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    # @staticmethod
    # def render_row_number(record, counter):
    #     return str(record['_id']['$oid'])

    @staticmethod
    def render_file_model_no(record: Files):
        if record.file_model_no == "0":
            return '<span class="label label-info label-tag">D0 - None</span>'
        return None

    @staticmethod
    def render_file_name(record: Files):
        return str(record.file_name)

    @staticmethod
    def render_file_size(record: Files):
        return str(filesizeformat(record.file_size))

    @staticmethod
    def render_file_type(record: Files):
        return str(record.file_type)

    @staticmethod
    def render_file_mime(record: Files):
        return str(record.file_mime)

    @staticmethod
    def render_file_path(record: Files):
        return str(record.file_path)

    @staticmethod
    def render_file_name_ext(record: Files):
        return str(record.file_name_ext)

    @staticmethod
    def render_file_parent_id(record: Files):
        return str(record.file_parent_id)

    @staticmethod
    def render_file_directory_code(record: Files):
        return str(record.file_directory_code)

    @staticmethod
    def render_file_directory_name(record: Files):
        return str(record.file_directory_name)

    @staticmethod
    def render_file_office_name(record: Files):
        return str(record.file_office_name)

    @staticmethod
    def render_file_office_type(record: Files):
        return str(record.file_office_type)

    @staticmethod
    def render_file_office_directory_code(record: Files):
        return str(record.file_office_directory_code)

    @staticmethod
    def render_file_office_directory_name(record: Files):
        return str(record.file_office_directory_name)

    @staticmethod
    def render_file_office_uploaded(record: Files):
        return str(record.file_office_uploaded)

    @staticmethod
    def render_file_created_at(record: Files):
        utc_dt = pytz.timezone(settings.TIME_ZONE).localize(
            datetime.datetime.fromtimestamp(record.file_created_at)
        )
        display_dt = utc_dt.astimezone(
            pytz.timezone(settings.APP_CONSTANT_DISPLAY_TIME_ZONE)
        )
        return naturaltime(display_dt)

    @staticmethod
    def render_file_created_id(record: Files):
        return str(record.file_created_id)

    @staticmethod
    def render_file_created_by(record: Files):
        return str(record.file_created_by)

    @staticmethod
    def render_file_updated_at(record: Files):
        utc_dt = pytz.timezone(settings.TIME_ZONE).localize(
            datetime.datetime.fromtimestamp(record.file_updated_at)
        )
        display_dt = utc_dt.astimezone(
            pytz.timezone(settings.APP_CONSTANT_DISPLAY_TIME_ZONE)
        )
        return naturaltime(display_dt)

    @staticmethod
    def render_file_updated_id(record: Files):
        return record.file_updated_id

    @staticmethod
    def render_file_updated_by(record: Files):
        return str(record.file_updated_by)

    @staticmethod
    def render_file_deleted_at(record: Files):
        utc_dt = pytz.timezone(settings.TIME_ZONE).localize(
            datetime.datetime.fromtimestamp(record.file_deleted_at)
        )
        display_dt = utc_dt.astimezone(
            pytz.timezone(settings.APP_CONSTANT_DISPLAY_TIME_ZONE)
        )
        return naturaltime(display_dt)

    @staticmethod
    def render_file_deleted_id(record: Files):
        return record.file_deleted_id

    @staticmethod
    def render_file_deleted_by(record: Files):
        return str(record.file_deleted_by)

    @staticmethod
    def render_file_status(record: Files):
        return str(record.file_status)

    class Meta:
        order_column_index = 1
        order_column_sort = "desc"
        attrs = {
            "id": "table-" + Files.NAME,
            "name": Files.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "file_model_no",
                },
                {
                    "data": "file_name",
                },
                {
                    "data": "file_size",
                },
                {
                    "data": "file_type",
                },
                {
                    "data": "file_mime",
                },
                {
                    "data": "file_path",
                },
                {
                    "data": "file_name_ext",
                },
                {
                    "data": "file_parent_id",
                },
                {
                    "data": "file_directory_code",
                },
                {
                    "data": "file_directory_name",
                },
                {
                    "data": "file_office_name",
                },
                {
                    "data": "file_office_type",
                },
                {
                    "data": "file_office_directory_code",
                },
                {
                    "data": "file_office_directory_name",
                },
                {
                    "data": "file_office_uploaded",
                },
                {
                    "data": "file_updated_at",
                },
                {
                    "data": "file_updated_by",
                },
                {
                    "data": "file_status",
                },
            ],
        }
        sequence = (
            "file_model_no",
            "file_name",
            "file_size",
            "file_type",
            "file_mime",
            "file_path",
            "file_name_ext",
            "file_parent_id",
            "file_directory_code",
            "file_directory_name",
            "file_office_name",
            "file_office_type",
            "file_office_directory_code",
            "file_office_directory_name",
            "file_office_uploaded",
            "file_updated_at",
            "file_updated_by",
            "file_status",
        )
        fields = (
            "file_model_no",
            "file_name",
            "file_size",
            "file_type",
            "file_mime",
            "file_path",
            "file_name_ext",
            "file_parent_id",
            "file_directory_code",
            "file_directory_name",
            "file_office_name",
            "file_office_type",
            "file_office_directory_code",
            "file_office_directory_name",
            "file_office_uploaded",
            "file_updated_at",
            "file_updated_by",
            "file_status",
        )
        template_name = "_include/bootstrap-datatable-server-files.html"
