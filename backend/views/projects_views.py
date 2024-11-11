import asyncio
import json
from datetime import timedelta

from django.contrib import messages
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from app import settings
from app.models.projects import Projects
from app.models.methods.projects import Methods_Projects
from app.models.methods.logs import Methods_Logs
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.status import Methods_Status
from app.models.methods.users import Methods_Users
from app.models.users import Users
from app.models.organizations import Organizations
from app.models.activities import Activities
from app.models.levels import Levels
from app.models.reports import Reports
#from app.models.divisions import Divisions
from app.utils import Utils
from backend.forms.projects_forms import (
    ProjectsCreateForm,
    ProjectsSearchIndexForm,
    ProjectsUpdateForm,
    ProjectsViewForm,
)
from backend.forms.activities_forms import (
    ActivitiesSearchIndexForm,
)
from backend.forms.implements_forms import(
    ImplementersCreateForm
)
from backend.forms.notifications_forms import(
     NotificationsCreateForm
)
from backend.forms.comments_forms import (
    CommentsAssignForm)
from backend.tables.projects_tables import ProjectsTable
from backend.tables.activities_tables import ActivitiesTable
from backend.tables.reports_tables import ReportsTable
from backend.tables.fundings_tables_view import FundingsTableView


class AjaxProjectsList(View):
    def get(self, request):
        user = Users.login_required(request)
        if user is None:
            return HttpResponse(
                json.dumps({}, cls=DjangoJSONEncoder), content_type="application/json"
            )
        items = self._datatables(request, user)
        return HttpResponse(
            json.dumps(items, cls=DjangoJSONEncoder), content_type="application/json"
        )

    def _datatables(self, request, user):
        auth_permissions = Methods_Users.get_auth_permissions(user)

        datatables = request.GET
        table_type = datatables.get('table')
        if table_type == 'projects':
            column1 = 'project_name'
            column2 = 'organization_id'
            column3 = 'project_start_date'
            column4 = 'project_deadline'
            column5 = 'project_updated_at'
            column6 = 'project_updated_by'
            column7 = 'project_status'

            # item draw
            draw = int(datatables.get("draw"))
            # item start
            start = int(datatables.get("start"))
            # item length (limit)
            length = int(datatables.get("length"))
            # item data search
            search = datatables.get("search[value]")

            # Get objects
            objects = Projects.objects
        
            # Get objects when you are data manager
            if user.user_role == Users.TYPE_ACTIVITY_MANAGER:
                objects = objects.filter(Q(organization_id=user.organization_id))
            
            if user.user_role == Users.TYPE_DATA_REPORTER:
                objects = objects.filter(Q(organization_id= user.organization_id) & Q(project_assigned_to=user.user_id))

            records_total = objects.all().count()
            # Set records filtered
            records_filtered = records_total

            order_column_index = datatables.get("order[0][column]")
            order_column_sort = datatables.get("order[0][dir]")

            if order_column_index and order_column_sort:
                if int(order_column_index) == 1:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column1)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column1)
                if int(order_column_index) == 2:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column2)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column2)
                if int(order_column_index) == 3:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column3)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column3)
                if int(order_column_index) == 4:
                    if order_column_sort == 'asc':
                        objects = objects.order_by(column4)
                    if order_column_sort == 'desc':
                        objects = objects.order_by('-' + column4)
                if int(order_column_index) == 5:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column5)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column5)
                if int(order_column_index) == 6:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column6)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column6)
                if int(order_column_index) == 7:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column7)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column7)

            objects_filter = False
            if search:
                objects_filter = True
                filter_users = Users.objects.filter(Q(user_name__icontains=search))
                if search == "-":
                    filter_organizations = [0]
                else:
                    filter_organizations = Organizations.objects.filter(
                        Q(organization_name__icontains=search)
                    )
                objects = objects.filter(
                    Q(project_name__icontains=search) |
                    Q(organization_id__in=filter_organizations) |
                    Q(project_start_date__icontains=search) |
                    Q(project_updated_by__in=filter_users)
                )

            column_index = 1
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                objects = objects.filter(Q(project_name__icontains=column_search))
            
            column_index = 2
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            
            if column_search != "":
                objects_filter = True
                
                if column_search == "-":
                    filter_organizations = [0]
                else:
                    filter_organizations = Organizations.objects.filter(
                        Q(organization_name__icontains=column_search)
                    )
                objects = objects.filter(Q(organization_id__in=filter_organizations))

            column_index = 3
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                date_time = Utils.convert_string_to_date(column_search)
                next_day = date_time  + timedelta(days=1)
                objects = objects.filter(
                    Q(project_start_date__gte=date_time )
                    & Q(project_start_date__lt=next_day)
                )


            column_index = 4
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                date_time_d = Utils.convert_string_to_date(column_search)
                next_day_d = date_time_d  + timedelta(days=1)
                objects = objects.filter(
                    Q(project_deadline__gte=date_time_d )
                    & Q(project_deadline__lt=next_day_d)
                )

            column_index = 5
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                seconds = (
                    Utils.convert_string_to_datetime(
                        Utils.get_format_input_date(column_search) + " 00:00:00"
                    )
                ).timestamp() + settings.TIME_DIFFERENCE
                objects = objects.filter(
                    Q(project_updated_at__gte=seconds)
                    & Q(project_updated_at__lt=(seconds + 86400))
                )

            column_index = 6
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                filter_users = Users.objects.filter(Q(user_name__icontains=column_search))
                objects = objects.filter(Q(project_updated_by__in=filter_users))

            column_index = 7
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                objects = objects.filter(
                    Q(project_status=Projects.ARRAY_TEXT_STATUS.index(column_search))
                )

            if objects_filter:
                records_filtered = objects.all().count()

            items = objects.all()

            if length == -1:
                paginator = Paginator(items, items.count())
                page_number = 1
            else:
                paginator = Paginator(items, length)
                page_number = start / length + 1

            try:
                object_list = paginator.page(page_number).object_list
            except PageNotAnInteger:
                object_list = paginator.page(1).object_list
            except EmptyPage:
                object_list = paginator.page(1).object_list

            counter = 0
            data = []
            for record in object_list:
                counter = counter + 1
                row_number = ProjectsTable.render_row_number(record, counter)
                value1 = ProjectsTable.render_project_name(record)
                value3 = ProjectsTable.render_organization_id(record)
                value6 = ProjectsTable.render_project_start_date(record)
                value7 = ProjectsTable.render_project_updated_at(record)
                value8 = ProjectsTable.render_project_updated_by(record)
                value9 = ProjectsTable.render_project_status(record)
                value10 = ProjectsTable.render_project_deadline(record)
                actions = ProjectsTable.render_actions(record, auth_permissions)

                data.append({
                    'row_number': row_number,
                    'project_name': value1,
                    'organization_id': value3,
                    'project_start_date': value6,
                    'project_deadline':value10,
                    'project_updated_at': value7,
                    'project_updated_by': value8,
                    'project_status': value9,
                    'actions': actions,
                })

            return {
                "draw": draw,
                "recordsTotal": records_total,
                "recordsFiltered": records_filtered,
                "data": data,
            }
        if table_type == 'activities':
            column1 = "activity_name"
            column2 = "project_id"
            column3 = "activity_location"
            column4 = "activity_fiscal_year"
            column5 = "activity_updated_at"
            column6 = "activity_updated_by"
            column7 = "activity_status"

            # datatables = request.GET
            # item draw
            draw = int(datatables.get("draw"))
            # item start
            start = int(datatables.get("start"))
            # item length (limit)
            length = int(datatables.get("length"))
            # item data search
            search = datatables.get("search[value]")

            project_id = datatables.get("project_id")
            # Get objects
            objects = Activities.objects.filter(Q(project_id=project_id))
            

            # if user.user_role== user.TYPE_ACTIVITY_MANAGER:
            #     objects = objects.exclude(Q(activity_status=Activities.STATUS_DRAFT))
            
            if user.user_role== user.TYPE_SUPER_ADMIN:
                objects = objects.exclude(Q(activity_status=Activities.STATUS_DRAFT))
            
            records_total = objects.all().count()
            # Set records filtered
            records_filtered = records_total

            order_column_index = datatables.get("order[0][column]")
            order_column_sort = datatables.get("order[0][dir]")

            if order_column_index and order_column_sort:
                if int(order_column_index) == 1:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column1)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column1)
                if int(order_column_index) == 2:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column2)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column2)
                if int(order_column_index) == 3:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column3)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column3)
                if int(order_column_index) == 4:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column4)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column4)
                if int(order_column_index) == 5:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column5)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column5)
                if int(order_column_index) == 6:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column6)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column6)
                if int(order_column_index) == 7:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column7)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column7)
            

            objects_filter = False
            if search:
                objects_filter = True
                filter_users = Users.objects.filter(Q(user_name__icontains=search))
                objects = objects.filter(
                    Q(activity_name__icontains=search)
                    | Q(activity_location__icontains=search)
                    | Q(activity_updated_by__in=filter_users)
                )

            column_index = 1
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                objects = objects.filter(Q(activity_name__icontains=column_search))
                
            column_index = 2
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                filter_projects = Projects.objects.filter(Q(project_name__icontains=column_search))
                objects = objects.filter(Q(project_id__in=filter_projects))

            column_index = 3
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                filter_locations = Levels.objects.filter(Q(level_name__icontains=column_search))
                objects = objects.filter(Q(activity_location__in=filter_locations))
                
            column_index = 4
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                objects = objects.filter(Q(activity_fiscal_year__icontains=column_search))

            column_index = 5
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                seconds = (
                    Utils.convert_string_to_datetime(
                        Utils.get_format_input_date(column_search) + " 00:00:00"
                    )
                ).timestamp() + settings.TIME_DIFFERENCE
                objects = objects.filter(
                    Q(activity_updated_at__gte=seconds)
                    & Q(activity_updated_at__lt=(seconds + 86400))
                )

            column_index = 6
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                filter_users = Users.objects.filter(Q(user_name__icontains=column_search))
                objects = objects.filter(Q(activity_updated_by__in=filter_users))

            column_index = 7
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
        
            if column_search != "": 
                objects_filter = True
                search = column_search.replace("^", "").replace("$", "")
                objects = objects.filter(
                    Q(activity_status=Activities.ARRAY_TEXT_STATUS.index(search))
                )

            if objects_filter:
                records_filtered = objects.all().count()

            items = objects.all()
            
            if length == -1:
                paginator = Paginator(items, items.count())
                page_number = 1
            else:
                paginator = Paginator(items, length)
                page_number = start / length + 1

            try:
                object_list = paginator.page(page_number).object_list
            except PageNotAnInteger:
                object_list = paginator.page(1).object_list
            except EmptyPage:
                object_list = paginator.page(1).object_list

            counter = 0
            data = []
            for record in object_list:
                counter = counter + 1
                row_numberA = ActivitiesTable.render_row_number(record, counter)
                valueA1 = ActivitiesTable.render_activity_name(record)
                valueA2 = ActivitiesTable.render_activity_location(record)
                valueA4 = ActivitiesTable.render_activity_updated_at(record)
                valueA5 = ActivitiesTable.render_activity_updated_by(record)
                valueA6 = ActivitiesTable.render_activity_status(record)
                valueA8 = ActivitiesTable.render_activity_fy(record)
                valueA9 = ActivitiesTable.render_activity_project(record)
                actionsA = ActivitiesTable.render_actions(record, auth_permissions)
                data.append(
                    {
                        "row_number": row_numberA,
                        "activity_name": valueA1,
                        "activity_location": valueA2,
                        "activity_updated_at": valueA4,
                        "activity_updated_by": valueA5,
                        "activity_status": valueA6,
                        "fiscal_year": valueA8,
                        "project_id": valueA9,
                        "actions": actionsA,
                    }
                )

            return {
                "draw": draw,
                "recordsTotal": records_total,
                "recordsFiltered": records_filtered,
                "data": data,
            }
            
            
        
        if table_type == 'capitals':
            column1 = "report_asset_name"
            column2 = "report_purchase_value"
            column3 = "report_year_purchased"
            column4 = "report_updated_at"
            column5 = "report_updated_by"
            column6 = "report_status"

            #datatables = request.GET
            # item draw
            draw = int(datatables.get("draw"))
            # item start
            start = int(datatables.get("start"))
            # item length (limit)
            length = int(datatables.get("length"))
            # item data search
            search = datatables.get("search[value]")
            project_id = datatables.get("project_id")

            # Get objects
            objects = Reports.objects.filter(Q(project_id=project_id))
            if user.user_role== user.TYPE_ACTIVITY_MANAGER:
                objects = objects.exclude(Q(report_status=Reports.STATUS_DRAFT))
            if user.user_role== user.TYPE_SUPER_ADMIN:
                objects = objects.filter(Q(report_status=Reports.STATUS_ACCEPTED)|Q(report_status=Reports.STATUS_APPROVED)| Q(report_status=Reports.STATUS_DENIED))
            records_total = objects.all().count()
            # Set records filtered
            records_filtered = records_total
            order_column_index = datatables.get("order[0][column]")
            order_column_sort = datatables.get("order[0][dir]")

            if order_column_index and order_column_sort:
                if int(order_column_index) == 1:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column1)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column1)
                if int(order_column_index) == 2:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column2)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column2)
                if int(order_column_index) == 3:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column3)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column3)
                if int(order_column_index) == 4:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column4)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column4)
                if int(order_column_index) == 5:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column5)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column5)
                if int(order_column_index) == 6:
                    if order_column_sort == "asc":
                        objects = objects.order_by(column6)
                    if order_column_sort == "desc":
                        objects = objects.order_by("-" + column6)

            objects_filter = False
            if search:
                objects_filter = True
                filter_users = Users.objects.filter(Q(user_name__icontains=search))
                objects = objects.filter(
                    Q(report_asset_name__icontains=search)
                    | Q(report_purchase_value__icontains=search)
                    | Q(report_year_purchased__icontains=search)
                    | Q(report_updated_by__in=filter_users)
                    | Q(report_status__icontains=search)
                )

            column_index = 1
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                objects = objects.filter(Q(report_asset_name__icontains=column_search))

            column_index = 2
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                objects = objects.filter(Q(report_purchase_value__icontains=column_search))

            column_index = 3
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                objects = objects.filter(Q(report_year_purchased__icontains=column_search))

            column_index = 4
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                seconds = (
                    Utils.convert_string_to_datetime(
                        Utils.get_format_input_date(column_search) + " 00:00:00"
                    )
                ).timestamp() + settings.TIME_DIFFERENCE
                objects = objects.filter(
                    Q(report_updated_at__gte=seconds)
                    & Q(report_updated_at__lt=(seconds + 86400))
                )

            column_index = 5
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                filter_users = Users.objects.filter(Q(user_name__icontains=column_search))
                objects = objects.filter(Q(report_updated_by__in=filter_users))

            column_index = 6
            column_search = datatables.get(
                "columns[" + str(column_index) + "][search][value]"
            )
            if column_search != "":
                objects_filter = True
                objects = objects.filter(
                    Q(report_status=Reports.ARRAY_TEXT_STATUS.index(column_search))
                )


            if objects_filter:
                records_filtered = objects.all().count()

            items = objects.all()

            if length == -1:
                paginator = Paginator(items, items.count())
                page_number = 1
            else:
                paginator = Paginator(items, length)
                page_number = start / length + 1

            try:
                object_list = paginator.page(page_number).object_list
            except PageNotAnInteger:
                object_list = paginator.page(1).object_list
            except EmptyPage:
                object_list = paginator.page(1).object_list

            counter = 0
            data = []
            for record in object_list:
                counter = counter + 1
                row_number = ReportsTable.render_row_number(record, counter)
                value1 = ReportsTable.render_report_asset_name(record)
                value2 = ReportsTable.render_report_purchase_value(record)
                value3 = ReportsTable.render_report_year_purchased(record)
                value4 = ReportsTable.render_report_updated_at(record)
                value5 = ReportsTable.render_report_updated_by(record)
                value6 = ReportsTable.render_report_status(record)
                actions = ReportsTable.render_actions(record, auth_permissions)
                data.append(
                    {
                        "row_number": row_number,
                        "report_asset_name": value1,
                        "report_purchase_value": value2,
                        "report_year_purchased": value3,
                        "report_updated_at": value4,
                        "report_updated_by": value5,
                        "report_status": value6,
                        "actions": actions,
                    }
                )

            return {
                "draw": draw,
                "recordsTotal": records_total,
                "recordsFiltered": records_filtered,
                "data": data,
            }


def json_projects(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_PROJECTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    return HttpResponse(
        serializers.serialize("json", Projects.objects.all()),
        content_type="application/json",
    )


def index(request):
    template_url = "projects/index.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    
    if settings.ACCESS_PERMISSION_PROJECTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    search_form = ProjectsSearchIndexForm(request.POST or None)
    if request.method == "POST" and search_form.is_valid():
        display_search = True
    else:
        display_search = False

    table = ProjectsTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_PROJECTS,
            "title": Projects.TITLE,
            "name": Projects.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "table": table,
            "search_form": search_form,
            "display_search": display_search,
            "index_url": reverse("projects_index"),
            "select_multiple_url": reverse("projects_select_multiple"),
        },
    )


@csrf_exempt
def select_single(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_PROJECTS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    action = request.POST["action"]
    id = request.POST["id"]
    
    if action == "" or id is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    try:
        model = Projects.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    if action == "block":
        if model.project_status == Methods_Status.STATUS_ACTIVE:
            Methods_Projects.update_status(
                request, user, model, Methods_Status.STATUS_BLOCKED
            )
            messages.success(request, "Blocked successfully.")

    if action == "unblock":
        if model.project_status == Methods_Status.STATUS_BLOCKED:
            Methods_Projects.update_status(
                request, user, model, Methods_Status.STATUS_ACTIVE
            )
            messages.success(request, "Unblocked successfully.")

    if action == "assign":
        # comments = request.POST['comments']
        to = request.POST['to']
        if settings.ACCESS_PERMISSION_PROJECTS_ASSIGN not in auth_permissions.values():
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if (
            model.project_status == model.STATUS_DRAFT or model.STATUS_ACTIVE
            or model.project_status == model.STATUS_ASSIGNED
        ):
            
            Methods_Projects.update_status(
                request, user, model, model.STATUS_ASSIGNED,None, to
                )
            messages.success(request, "Assigned successfully.")

    if action == "delete":
        if settings.ACCESS_PERMISSION_PROJECTS_DELETE not in auth_permissions.values():
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        Methods_Projects.delete(request, user, model)
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")


@csrf_exempt
def select_multiple(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_PROJECTS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    action = request.POST["action"]
    ids = request.POST["ids"]
    try:
        ids = ids.split(",")
    except (TypeError, ValueError, OverflowError):
        ids = None
    if action == "" or ids is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    if action == "block":
        for id in ids:
            try:
                model = Projects.objects.get(pk=id)
                if model.project_status == Methods_Status.STATUS_ACTIVE:
                    Methods_Projects.update_status(
                        request, user, model, Methods_Status.STATUS_BLOCKED
                    )
            except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
                continue
        messages.success(request, "Blocked successfully.")

    if action == "unblock":
        for id in ids:
            try:
                model = Projects.objects.get(pk=id)
                if model.project_status == Methods_Status.STATUS_BLOCKED:
                    Methods_Projects.update_status(
                        request, user, model, Methods_Status.STATUS_INACTIVE
                    )
            except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
                continue
        messages.success(request, "Unblocked successfully.")

    if action == "delete":
        if settings.ACCESS_PERMISSION_PROJECTS_DELETE not in auth_permissions.values():
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        for id in ids:
            try:
                model = Projects.objects.get(pk=id)
                Methods_Projects.delete(request, user, model)
            except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
                continue
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")


def create(request):
    template_url = "projects/create.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_PROJECTS_CREATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    form_implementers =ImplementersCreateForm(user=None)
    if request.method == "POST":
        form = ProjectsCreateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "name": form.cleaned_data['name'],
                "financing_agent": form.cleaned_data['financing_agent'],
                'implementer': form.cleaned_data['implementer'],
                "organization_id": form.cleaned_data['organization_id'],
                "start_time": form.cleaned_data['start_time'],
                "deadline": form.cleaned_data['deadline'],
            }
            err, msg, model = Methods_Projects.create(request, user, data)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_PROJECTS,
                        "title": Projects.TITLE,
                        "name": Projects.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                        "form_implementers": form_implementers
                    },
                )
            messages.success(request, "Created successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_PROJECTS,
                    model.project_id,
                    "Created projects.",
                    user.user_id,
                    user.user_name,
                )
            )
        #     return JsonResponse({'project_id': model.project_id, 'message':"success"})
        # else:
        #     return HttpResponse(str(form.errors), content_type="text/plain")
            return redirect(reverse("projects_view", args=[model.project_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_PROJECTS,
                    "title": Projects.TITLE,
                    "name": Projects.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "form_implementers":form_implementers
                },
            )

    form = ProjectsCreateForm(user=user)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_PROJECTS,
            "title": Projects.TITLE,
            "name": Projects.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "form_implementers": form_implementers
        },
    )


def update(request, pk):
    template_url = "projects/update.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_PROJECTS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Projects.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    if request.method == "POST":
        form = ProjectsUpdateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "name": form.cleaned_data['name'],
                "financing_agent": form.cleaned_data['financing_agent'],
                'implementer': form.cleaned_data['implementer'],
                "organization_id": form.cleaned_data['organization_id'],
                "start_time": form.cleaned_data['start_time'],
                "deadline": form.cleaned_data['deadline'],
                "assign_to": form.cleaned_data['assign_to']
            }
            err, msg, model = Methods_Projects.update(request, user, data, model)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_PROJECTS,
                        "title": Projects.TITLE,
                        "name": Projects.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                        "model": model,
                    },
                )
            messages.success(request, "Updated successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_PROJECTS,
                    model.project_id,
                    "Updated projects.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("projects_view", args=[model.project_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_PROJECTS,
                    "title": Projects.TITLE,
                    "name": Projects.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "model": model,
                },
            )
    form = ProjectsUpdateForm(
        user=user, initial=Methods_Projects.form_view(request, user, model)
    )
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_PROJECTS,
            "title": Projects.TITLE,
            "name": Projects.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "model": model,
        },
    )


def view(request, pk):
    template_url = "projects/view.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_PROJECTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Projects.objects.get(pk=pk)
        organization_id = model.organization_id
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    model = Methods_Projects.format_view(request, user, model)
    form = ProjectsViewForm(
        user=user, initial=Methods_Projects.form_view(request, user, model)
    )
    form_comments_assign = CommentsAssignForm(user=user)
    form_notifications = NotificationsCreateForm(user = user, project_id = model.project_id)
 
    count_logs = Methods_Mongo.get_collection(settings.MODEL_LOGS).count_documents(
        {"model": "organizations", "modelId": model.project_id}
    )

    search_form_activities = ActivitiesSearchIndexForm(request.POST or None)
    if request.method == "POST" and search_form_activities.is_valid():
        display_search_activities = True
    else:
        display_search_activities = False
    table_activities = ActivitiesTable({})
    table_activities.set_auth_permissions(auth_permissions)

    table_reports = ReportsTable({})
    table_reports.set_auth_permissions(auth_permissions)

    table_fundings =FundingsTableView({})
    table_fundings.set_auth_permissions(auth_permissions)



    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_PROJECTS,
            "title": Projects.TITLE,
            "name": Projects.NAME,
            "organization_id": organization_id,
            "user": user,
            "auth_permissions": auth_permissions,
            "model": model,
            "form": form,
            "index_url": reverse("projects_index"),
            "select_single_url": reverse("projects_select_single"),
            "count_logs": count_logs,
            "table_activities": table_activities,
            "table_reports":table_reports,
            "table_fundings":table_fundings,
            "form_comments_assign":form_comments_assign,
            "form_notifications":form_notifications,
            "search_form": search_form_activities,
            "display_search": display_search_activities,
        },
    )

def extract_year(date):
    return date.year

def get_financing_agents(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    values = ""
    try:
        organizations = Organizations.objects.filter(organization_category__icontains=Organizations.STATUS_FINANCING)
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain") 
    values = "<option value='0' >--Select--</option>"
    for organization in organizations:
            values += (
            "<option value='"
            + str(organization.organization_id)
            + "'>"
            + str(organization.organization_name)
            + "</option>"
        )           
    return HttpResponse(values, content_type="text/plain")
