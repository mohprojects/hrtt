from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
#from app.models.divisions import Divisions
from app.models.fundings import Fundings
from app.models.methods.status import Methods_Status
from app.models.organizations import Organizations
from app.models.projects import Projects
from app.models.users import Users
from app.utils import Utils


class ProjectsTable(tables.Table):
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
    project_name = tables.Column(
        verbose_name="Name",
        attrs={
            "search_filter": "input-text",
        },
    )
    # project_financing_agent = tables.Column(
    #     verbose_name='Financing Agent',
    #     attrs={
    #         "search_filter": "input-text",
    #     },
    # )
    organization_id = tables.Column(
        verbose_name="Organization",
        attrs={
            "search_filter": "input-text",
        },
    )
    project_start_date = tables.Column(
        verbose_name='Start Date',
        attrs={
            'search_filter': 'input-date',
        }
    )
    project_deadline = tables.Column(
        verbose_name='End Date',
        attrs={
            "search_filter": "input-date",
        },
    )
    project_updated_at = tables.Column(
        verbose_name="Updated At",
        attrs={
            "search_filter": "input-date",
        },
    )
    project_updated_by = tables.Column(
        verbose_name="Updated By",
        attrs={
            "search_filter": "input-text",
        },
    )
    project_status = tables.Column(
        verbose_name="Status",
        attrs={
            "search_filter": "input-select",
            "search_data": Projects.ARRAY_TEXT_STATUS,
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
        super(ProjectsTable, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = "<a href=" + str(record.pk) + ">" + "%d" % counter + "</a>"
        return value

    @staticmethod
    def render_actions(record, auth_permissions):
        data = ""
        if settings.ACCESS_PERMISSION_PROJECTS_VIEW in auth_permissions.values():
            url = reverse("projects_view", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-eye"></i></button>&nbsp;'
            )
        if settings.ACCESS_PERMISSION_PROJECTS_UPDATE in auth_permissions.values():
            url = reverse("projects_update", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-edit"></i></button>&nbsp;'
            )
        if settings.ACCESS_PERMISSION_PROJECTS_DELETE in auth_permissions.values():
            url = reverse("projects_select_single")
            data += (
                '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\''
                + url
                + "', 'delete', '"
                + str(record.pk)
                + '\');" ><i class="fa fa-trash"></i></button>&nbsp;'
            )
        return data

    @staticmethod
    def render_project_name(record: Projects):
        return mark_safe(
            "<a href="
            + reverse("projects_view", args=[record.pk])
            + " style='text-decoration:underline; color:#1B82DC;' >"
            + str(record.project_name)
            + "</a>"
        )

    # @staticmethod
    # def render_project_financing_agent(record: Projects):
    #     financing_agents_ids= record.project_financing_agent
    #     resp = "<div class='center-block' style='text-align: left;list-style: square;' >"
    #     financing_agents_ids = financing_agents_ids.strip('][')
    #     if len(financing_agents_ids)>0:
    #         res = ""
    #         financing_agents_ids = financing_agents_ids.strip(' ').replace("'","").split(',')
    #         for id in financing_agents_ids: 
    #             try: 
    #                 financing_agent = Organizations.objects.get(pk= int(id))
    #                 if financing_agent:
    #                     res = res + "<span class='badge badge-secondary'>"+ financing_agent.organization_name + "</span>"
    #             except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
    #                 res = ""
    #         resp = resp + res + "</div>"
    #         return resp
    #     return ""
    
    @staticmethod
    def render_project_deadline(record: Projects):
        return str(record.project_deadline)
    
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
    def render_project_start_date(record: Projects):
        return str(record.project_start_date)

    @staticmethod
    def render_project_updated_at(record: Projects):
        return (
            Utils.get_convert_datetime(
                record.project_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

    @staticmethod
    def render_project_updated_by(record: Projects):
        try:
            user = Users.objects.get(pk=record.project_updated_by)
            return str(user.user_name)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            return "-"

    @staticmethod
    def render_project_status(record: Projects):
        value = ''
        if record.project_status == Projects.STATUS_DRAFT:
            value = Projects.HTML_TAG_STATUS_DRAFT_COLOR
            return value
        if record.project_status == Projects.STATUS_ACTIVE:
            value = Projects.HTML_TAG_STATUS_ACTIVE_COLOR
            return value

        if record.project_status == Projects.STATUS_ASSIGNED:
            value = Projects.HTML_TAG_STATUS_ASSIGNED_COLOR
            return value
        elif record.project_status == Projects.STATUS_BLOCKED:
            value = Projects.HTML_TAG_STATUS_BLOCKED_COLOR
            
        return value

    class Meta:
        model = Projects
        order_column_index = 1
        order_column_sort = "asc"
        attrs = {
            "id": "table-" + Projects.NAME,
            "name": Projects.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "row_number",
                },
                {
                    "data": "project_name",
                },
                # {
                #     "data": "project_financing_agent",
                # },
                {
                    "data": "organization_id",
                },
                {
                    "data": "project_start_date",
                },
                {
                    "data": "project_deadline",
                },
                {
                    "data": "project_updated_at",
                },
                {
                    "data": "project_updated_by",
                },
                {
                    "data": "project_status",
                },
                {
                    "data": "actions",
                },
            ],
        }
        sequence = (
            'row_number',
            'project_name',
            # 'project_financing_agent',
            'organization_id',
            'project_start_date',
            'project_deadline',
            'project_updated_at',
            'project_updated_by',
            'project_status',
            'actions'
        )
        fields = (
            'project_name',
            # 'project_financing_agent',
            'organization_id',
            'project_start_date',
            'project_deadline',
            'project_updated_at',
            'project_updated_by',
            'project_status',
        )
        template_name = "_include/bootstrap-datatable-server.html"
