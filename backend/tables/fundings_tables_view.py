from __future__ import unicode_literals

import itertools
from django.urls import reverse
from django.utils.safestring import mark_safe
import django_tables2 as tables
from app import settings
from app.models.fundings import Fundings
from app.models.organizations import Organizations
from app.models.files import Files
from app.models.users import Users
from app.utils import Utils


class FundingsTableView(tables.Table):
    auth_permissions = {}

    row_number = tables.Column(
        verbose_name='Id',
        attrs={
            'search_filter': '',
            'th_style': 'width:60px;',
        },
        orderable=False,
        empty_values=(),
        accessor='pk',
    )

    funder_id = tables.Column(
        verbose_name="Funding Source",
        attrs={
            "search_filter": "input-text",
        },
    )
    funding_amount = tables.Column(
        verbose_name="Amount",
        attrs={
            "search_filter": "input-text",
        },
    )
    funding_currency= tables.Column(
        verbose_name="Currency",
        attrs={
            "search_filter": "input-text",
        },
    )
    funding_updated_at = tables.Column(
        verbose_name="Updated At",
        attrs={
            "search_filter": "input-date",
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
        super(FundingsTableView, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = "<a href=" + str(record.pk) + ">" + "%d" % counter + "</a>"
        return value

    @staticmethod
    def render_funder_id(record: Fundings):
        if record.funder_id != 0:
            try:
                item = Organizations.objects.get(pk=record.funder_id)
                return str(item.organization_name)
            except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                return "-"
        else:
            return "-"

    @staticmethod
    def render_funding_amount(record: Fundings):
        return Utils.format_amount_with_commas(record.funding_amount)
    
    @staticmethod
    def render_funding_currency(record: Fundings):
        return str(record.funding_currency)

    @staticmethod
    def render_funding_updated_at(record: Fundings):
        return (
            Utils.get_convert_datetime(
                record.funding_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

    @staticmethod
    def render_actions(record, auth_permissions,user:Users, project_organization):
        data = ""
        if user.organization_id == project_organization or user.user_role == Users.TYPE_SUPER_ADMIN :
            if settings.ACCESS_PERMISSION_PROJECTS_VIEW in auth_permissions.values():
                
                url = reverse("fundings_view", args=[record.pk])
                data += (
                    '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \''
                    + url
                    + '\';"><i class="fa fa-eye"></i></button>&nbsp;'
                )
            if settings.ACCESS_PERMISSION_PROJECTS_UPDATE in auth_permissions.values():
                url = reverse("fundings_update", args=[record.pk])
                data += (
                    '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \''
                    + url
                    + '\';"><i class="fa fa-edit"></i></button>&nbsp;'
                )
            if settings.ACCESS_PERMISSION_PROJECTS_DELETE in auth_permissions.values():
                url = reverse("fundings_select_single")
                data += (
                    '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\''
                    + url
                    + "', 'delete', '"
                    + str(record.pk)
                    + '\');" ><i class="fa fa-trash"></i></button>&nbsp;'
                )
        return data

    class Meta:
        order_column_index = 1
        order_column_sort = "desc"
        attrs = {
            "id": "table-" + Fundings.NAME,
            "name": Fundings.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                 {
                    "data": "row_number",
                },
                {
                    "data": "funder_id",
                },
                {
                    "data": "funding_amount",
                },
                {
                    "data": "funding_currency",
                },
                {
                    "data": "funding_updated_at",
                },
                {
                    "data": "actions",
                },
            ],
        }
        sequence = (
            "row_number",
            "funder_id",
            "funding_amount",
            "funding_currency",
            "funding_updated_at",
            "actions",
        )
        fields = (
            "row_number",
            "funder_id",
            "funding_amount",
            "funding_currency",
            "funding_updated_at",
        )
        template_name = "_include/bootstrap-datatable-server.html"
