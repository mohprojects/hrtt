from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.methods.status import Methods_Status
from app.models.activities_inputs import Activities_Inputs
from app.models.activities import Activities
from app.models.projects import Projects
from app.models.users import Users
from app.models.levels import Levels
from app.models.organizations import Organizations
from app.models.implementers import Implementers
from app.utils import Utils


class ActivitiesInputsTable(tables.Table):
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

    activity_input_class = tables.Column(
        verbose_name="Input Class",
        attrs={
            "search_filter": "input-text",
        },
    )
    activity_input_sub_class = tables.Column(
        verbose_name="Input Sub Class ",
        attrs={
            "search_filter": "input-text",
        },
    )
    activity_input_funder = tables.Column(
        verbose_name="Funder",
        attrs={
            "search_filter": "input-text",
        },
    )
    activity_input_funds_transfer_class = tables.Column(
        verbose_name="Transfer Class",
        attrs={
            "search_filter": "input-text",
        },
    )
    activity_input_funds_transfer_sub_class = tables.Column(
        verbose_name="Transfer Sub Class",
        attrs={
            "search_filter": "input-text",
        },
    )
    activity_input_implementer = tables.Column(
        verbose_name="Implementer",
        attrs={
            "search_filter": "input-text",
        },
    )
    activity_input_division = tables.Column(
        verbose_name="Division",
        attrs={
            "search_filter": "input-text",
        },
    )
  
    activity_input_budget = tables.Column(
        verbose_name="Budget Amount",
        attrs={
            "search_filter": "input-text",
        },
    )
    activity_input_expenses = tables.Column(
        verbose_name="Expenditure ",
        attrs={
            "search_filter": "input-text",
        },
    )
    activity_input_status = tables.Column(
        verbose_name="Status",
        attrs={
            "search_filter": "input-select",
            "search_data": Activities_Inputs.ARRAY_TEXT_STATUS,
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
    activity_input_double_count = tables.Column(
        verbose_name="Double Count",
        attrs={
            "search_filter": "input-text",
        },
    )

    def __init__(self, *args, **kwargs):
        self.counter = itertools.count(1)
        super(ActivitiesInputsTable, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = "<a href=" + str(record.pk) + ">" + "%d" % counter + "</a>"
        return value

    @staticmethod
    def render_actions(record:Activities_Inputs, auth_permissions):
        data = ""
        activity = Activities.objects.get(activity_id = record.activity_id)

        if settings.ACCESS_PERMISSION_ACTIVITIES_VIEW in auth_permissions.values():
            url = reverse("activities_inputs_view", args=[record.pk])
            data += (
                '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \''
                + url
                + '\';"><i class="fa fa-eye"></i></button><br>'
            )
        if (activity.activity_status == activity.STATUS_DRAFT or activity.activity_status == activity.STATUS_BUDGET_REJECTED  or 
            activity.activity_status == activity.STATUS_EXPENSES_REJECTED or 
            (activity.activity_status == activity.STATUS_SUBMITTED and record.activity_input_status == record.STATUS_BUDGET_REJECTED)) :
            if settings.ACCESS_PERMISSION_ACTIVITIES_UPDATE in auth_permissions.values():
                url = reverse("activities_inputs_update", args=[record.pk])
                data += (
                    '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \''
                    + url
                    + '\';"><i class="fa fa-edit"></i></button><br>'
                )
            if settings.ACCESS_PERMISSION_ACTIVITIES_DELETE in auth_permissions.values():
                url = reverse("activities_inputs_select_single")
                data += (
                    '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\''
                    + url
                    + "', 'delete', '"
                    + str(record.pk)
                    + '\');" ><i class="fa fa-trash"></i></button><br>'
                )
        return data

    @staticmethod
    def render_input_class(record: Activities_Inputs):
        try:
            item= Levels.objects.get(pk=record.activity_input_class)
            return mark_safe("<a href="
            + reverse("activities_inputs_view", args=[record.pk])
            + " style='text-decoration:underline; color:#1B82DC;' >"
            +str(item.level_name)+ "</a>")
        
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            return('')

    @staticmethod
    def render_input_sub_class(record: Activities_Inputs):
        try:
            item= Levels.objects.get(pk=record.activity_input_sub_class)
            return mark_safe(str(item.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            return('')
    
    @staticmethod
    def render_funder(record: Activities_Inputs):
        try:
            item= Organizations.objects.get(pk=record.activity_input_funder)
            return mark_safe(str(item.organization_name))
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            return('')
      

    @staticmethod
    def render_funder_transfer_class(record: Activities_Inputs):
        try:
            item= Levels.objects.get(pk=record.activity_input_funds_transfer_class)
            return mark_safe(str(item.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            return('')
        
    
    @staticmethod
    def render_funder_transfer_sub_class(record: Activities_Inputs):
        try:
            item= Levels.objects.get(pk=record.activity_input_funds_transfer_sub_class)
            return mark_safe(str(item.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            return('')
      
    
    @staticmethod
    def render_activity_implementer(record: Activities_Inputs):
        id = record.activity_input_implementer  
        if "_" in id:
            org_impl= id.split('_')
            if org_impl[0].strip(' ') == 'impl':
                try:
                    implementer = Implementers.objects.get(pk= int(org_impl[1]))
                    return mark_safe(str(implementer.implementer_name))
                except (TypeError, ValueError, OverflowError, Implementers.DoesNotExist):
                    return('')
        else:
            try:
                item= Organizations.objects.get(pk=int(id))
                return mark_safe(str(item.organization_name))
            except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                return('')
     
    
    @staticmethod
    def render_activity_division(record: Activities_Inputs):
        return str(record.activity_input_division)
    
    @staticmethod
    def render_activity_double_count(record: Activities_Inputs):
        data = ""
        value = record.activity_input_double_count
        url = reverse("activities_inputs_select_single")
        if value == 0:
            data += (
                    '<button class = "demo-delete-row btn btn-dark btn-sm" onclick="javascript: singleSelect(\''
                    + url
                    + "', 'double_count_yes', '"
                    + str(record.pk)
                    + '\');" ><i class="fa fa-times"></i></button>&nbsp'
                )
        if value == 1:
            data += (
                    '<button class = "demo-delete-row btn btn-dark btn-sm" onclick="javascript: singleSelect(\''
                    + url
                    + "', 'double_count_no', '"
                    + str(record.pk)
                    + '\');" ><i class="fa fa-check"></i></button>&nbsp'
                )
           
        return data
    
    @staticmethod
    def render_activity_budget(record: Activities_Inputs):
        budget = record.activity_input_budget
        budget_currency = record.activity_input_budget_currency
        return Utils.format_amount_with_commas(budget) + " "+ budget_currency
    
    @staticmethod
    def render_activity_expenses(record: Activities_Inputs):
        expenses = record.activity_input_expenses
        if expenses > 0.00:
            expenses_currency = record.activity_input_expenses_currency
            # return str(expenses) + " "+ expenses_currency
            return mark_safe("<a href="
            + reverse("activities_inputs_expenditure", args=[record.pk])
            + " style='text-decoration:underline; color:#1B82DC;' >"
            +Utils.format_amount_with_commas(expenses)+ " "+ expenses_currency + "</a>")
        
        else:
            # url = '#'
            
            if record.activity_input_status == Activities_Inputs.STATUS_DRAFT or record.activity_input_status == Activities_Inputs.STATUS_BUDGET_ACCEPTED or record.activity_input_status == Activities_Inputs.STATUS_BUDGET_REJECTED:
                data = (
                        '<div style="color:red;padding:20px">Budget Should be approved first</div>&nbsp'
                    )
            else:
                url = reverse("activities_inputs_expenditure", args=[record.pk])
                data = (
                        '<button class="demo-delete-row btn btn-success btn-xs" onclick="javascript:location.href = \''
                        + url
                        + '\';">Add Expenditure</i></button>&nbsp'
                    )
            return data
        
    @staticmethod
    def render_activity_input_status(record: Activities_Inputs):
        if record.activity_input_status == Activities_Inputs.STATUS_DRAFT:
            value = Activities_Inputs.HTML_TAG_STATUS_DRAFT_COLOR
            return value
        if record.activity_input_status == Activities_Inputs.STATUS_BUDGET_ACCEPTED:
            value = Activities_Inputs.HTML_TAG_STATUS_BUDGET_ACCEPTED_COLOR
            return value
        if record.activity_input_status == Activities_Inputs.STATUS_BUDGET_REJECTED:
            value = Activities_Inputs.HTML_TAG_STATUS_BUDGET_REJECTED_COLOR
            return value
        if record.activity_input_status == Activities_Inputs.STATUS_BUDGET_APPROVED:
            value =Activities_Inputs.HTML_TAG_STATUS_BUDGET_APPROVED_COLOR
            return value
        if record.activity_input_status == Activities_Inputs.STATUS_BUDGET_DENIED:
            value =Activities_Inputs.HTML_TAG_STATUS_BUDGET_DENIED_COLOR
            return value
        if record.activity_input_status == Activities_Inputs.STATUS_EXPENSES_ACCEPTED:
            value = Activities_Inputs.HTML_TAG_STATUS_EXPENSES_ACCEPTED_COLOR
            return value
        if record.activity_input_status == Activities_Inputs.STATUS_EXPENSES_REJECTED:
            value = Activities_Inputs.HTML_TAG_STATUS_EXPENSES_REJECTED_COLOR
            return value
        if record.activity_input_status == Activities_Inputs.STATUS_EXPENSES_APPROVED:
            value = Activities_Inputs.HTML_TAG_STATUS_EXPENSES_APPROVED_COLOR
            return value
        if record.activity_input_status == Activities_Inputs.STATUS_EXPENSES_DENIED:
            value = Activities_Inputs.HTML_TAG_STATUS_EXPENSES_DENIED_COLOR
            return value


    class Meta:
        model = Activities_Inputs

        order_column_index = 1
        order_column_sort = "asc"
        attrs = {
            "id": "table-" + Activities_Inputs.NAME,
            "name": Activities_Inputs.NAME,
            "class": "table table-bordered table-hover thead-dark table-responsive",
            "cellspacing": "0",
            "width": "100%",
            "default_order": [order_column_index, order_column_sort],
            "table_columns": [
                {
                    "data": "row_number",
                },
                {
                    "data": "activity_input_class",
                },
                 {
                    "data": "activity_input_sub_class",
                },
    
                {
                    "data": "activity_input_funder",
                },
                {
                    "data": "activity_input_funds_transfer_class",
                },
                {
                    "data": "activity_input_funds_transfer_sub_class",
                },
                {
                    "data": "activity_input_implementer",
                },
                {
                    "data": "activity_input_division",
                },
                
                {
                    "data": "activity_input_budget",
                },
                {
                    "data": "activity_input_expenses",
                },
                {
                    "data": "activity_input_status",
                },
                {
                    "data": "actions",
                },
                {
                  "data": "activity_input_double_count"  
                },
            ],
        }
        sequence = (
            "row_number",
            "activity_input_class",
            "activity_input_sub_class",
            "activity_input_funder",
            "activity_input_funds_transfer_class",
            "activity_input_funds_transfer_sub_class",
            "activity_input_implementer",
            "activity_input_division",
            "activity_input_budget",
            "activity_input_expenses",
            "activity_input_status",
            "actions",
            "activity_input_double_count",
        )
        fields = (
            "activity_input_class",
            "activity_input_sub_class",
            "activity_input_funder",
            "activity_input_funds_transfer_class",
            "activity_input_funds_transfer_sub_class",
            "activity_input_implementer",
            "activity_input_division",
            "activity_input_budget",
            "activity_input_expenses",
            "activity_input_status",
            "activity_input_double_count",
        )
      
        #template_name = "_include/bootstrap-datatable-server-activities.html"
        template_name = "_include/bootstrap-datatable-server.html"
