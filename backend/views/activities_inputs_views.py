import asyncio
import json

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
from app.models.activities_inputs import Activities_Inputs
from app.models.methods.activities_inputs import Methods_Activities_Inputs
from app.models.methods.activities import Methods_Activities
from app.models.activities import Activities
from app.models.projects import Projects
from app.models.organizations import Organizations
from app.models.levels import Levels
from app.models.implementers import Implementers
from app.models.methods.logs import Methods_Logs
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.users import Methods_Users
from app.models.methods.organizations import Methods_Organizations
from app.models.users import Users
from backend.forms.activities_inputs_forms import (
    ActivitiesInputsCreateForm,
    ActivitiesInputsSearchIndexForm,
    ActivitiesInputsUpdateForm,
    ActivitiesInputsViewForm,
    ActivitiesInputsExpenditureForm,
)
from backend.forms.comments_forms import (
    CommentsCreateForm,
    # CommentsCreateHtmlForm,
)
from backend.forms.fundings_forms import FundingsCreateForm
from backend.tables.activities_inputs_tables import ActivitiesInputsTable

DOUBLE_COUNT_ORG_TYPE = ["1", "4"]
DOUBLE_COUNT_TRANSFER = ["FS.3", "FS.4", "FS.5", "FS.7"]
DOUBLE_COUNT_SUB_TRANSFER = ["FS2.1","FS2.2"]


class AjaxActivitiesInputsList(View):
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

        column1 = "activity_input_class"
        column2 = "activity_input_sub_class"
        column3 = "activity_input_funder"
        column4 = "activity_input_funds_transfer_class"
        column5 = "activity_input_funds_transfer_sub_class"
        column6 = "activity_input_implementer"
        column7 = "activity_input_division"
        column8 = "activity_input_budget"
        column9 = "activity_input_expenses"
        column10 = "activity_input_status"

        datatables = request.GET
        # item draw
        draw = int(datatables.get("draw"))
        # item start
        start = int(datatables.get("start"))
        # item length (limit)
        length = int(datatables.get("length"))
        # item data search
        search = datatables.get("search[value]")

        activity_id = datatables.get("activity_id")

        # Get objects
        objects = Activities_Inputs.objects.filter(Q(activity_id=activity_id))

        if user.user_role == Users.TYPE_SUPER_ADMIN:
            objects = objects.exclude(
                Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_REJECTED)
            )

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
            if int(order_column_index) == 8:
                if order_column_sort == "asc":
                    objects = objects.order_by(column8)
                if order_column_sort == "desc":
                    objects = objects.order_by("-" + column8)
            if int(order_column_index) == 9:
                if order_column_sort == "asc":
                    objects = objects.order_by(column9)
                if order_column_sort == "desc":
                    objects = objects.order_by("-" + column9)
            if int(order_column_index) == 10:
                if order_column_sort == "asc":
                    objects = objects.order_by(column10)
                if order_column_sort == "desc":
                    objects = objects.order_by("-" + column10)

        objects_filter = False
        if search:
            objects_filter = True
            filter_users = Users.objects.filter(Q(user_name__icontains=search))
            objects = objects.filter(
                Q(activity_input_class__icontains=search)
                | Q(activity_input_sub_class__icontains=search)
                | Q(activity_input_funder__icontains=search)
                | Q(activity_input_funds_transfer_class__contains=search)
                | Q(activity_input_funds_transfer_sub_class__icontains=search)
                | Q(activity_input_implementer__icontains=search)
                | Q(activity_input_division__icontains=search)
                | Q(activity_input_budget__icontains=search)
                | Q(activity_input_expenses__icontains=search)
            )

        column_index = 1
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )

        if column_search != "":
            objects_filter = True
            filter_levels = Levels.objects.filter(
                Q(level_name__icontains=column_search)
            )
            objects = objects.filter(Q(activity_input_class__in=filter_levels))

        column_index = 2
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            filter_levels = Levels.objects.filter(
                Q(level_name__icontains=column_search)
            )
            objects = objects.filter(Q(activity_input_sub_class__in=filter_levels))

        column_index = 3
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            filter_organizations = Organizations.objects.filter(
                Q(organization_name__icontains=column_search)
            )
            objects = objects.filter(Q(activity_input_funder__in=filter_organizations))

        column_index = 4
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            filter_levels = Levels.objects.filter(
                Q(level_name__icontains=column_search)
            )
            objects = objects.filter(
                Q(activity_input_funds_transfer_class__in=filter_levels)
            )

        column_index = 5
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            filter_levels = Levels.objects.filter(
                Q(level_name__icontains=column_search)
            )
            objects = objects.filter(
                Q(activity_input_funds_transfer_sub_class__in=filter_levels)
            )

        column_index = 6
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            print(column_search)
            objects_filter = True
            filter_organizations = Organizations.objects.filter(
                Q(organization_name__icontains=column_search)
            )
            filter_implementers = Implementers.objects.filter(
                Q(implementer_name__icontains=column_search)
            )
            objects = objects.filter(
                Q(activity_input_implementer__in=filter_organizations)
            )

        column_index = 7
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            objects = objects.filter(
                Q(activity_input_division__icontains=column_search)
            )

        column_index = 8
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            objects = objects.filter(Q(activity_input_budget__icontains=column_search))

        column_index = 9
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            objects = objects.filter(
                Q(activity_input_expenses__icontains=column_search)
            )

        column_index = 10
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            objects = objects.filter(
                Q(
                    activity_input_status=Activities_Inputs.ARRAY_TEXT_STATUS.index(
                        column_search
                    )
                )
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
            row_number = ActivitiesInputsTable.render_row_number(record, counter)
            value1 = ActivitiesInputsTable.render_input_class(record)
            value2 = ActivitiesInputsTable.render_input_sub_class(record)
            value5 = ActivitiesInputsTable.render_funder(record)
            value6 = ActivitiesInputsTable.render_funder_transfer_class(record)
            value7 = ActivitiesInputsTable.render_funder_transfer_sub_class(record)
            value8 = ActivitiesInputsTable.render_activity_implementer(record)
            value9 = ActivitiesInputsTable.render_activity_division(record)
            value10 = ActivitiesInputsTable.render_activity_budget(record)
            value11 = ActivitiesInputsTable.render_activity_expenses(record)
            value12 = ActivitiesInputsTable.render_activity_input_status(record)
            actions = ActivitiesInputsTable.render_actions(record, auth_permissions)
            value13 = ActivitiesInputsTable.render_activity_double_count(record)

            data.append(
                {
                    "row_number": row_number,
                    "activity_input_class": value1,
                    "activity_input_sub_class": value2,
                    "activity_input_funder": value5,
                    "activity_input_funds_transfer_class": value6,
                    "activity_input_funds_transfer_sub_class": value7,
                    "activity_input_implementer": value8,
                    "activity_input_division": value9,
                    "activity_input_budget": value10,
                    "activity_input_expenses": value11,
                    "activity_input_status": value12,
                    "actions": actions,
                    "activity_input_double_count": value13,
                }
            )

        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }


def json_activities_inputs(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ACTIVITIES_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    return HttpResponse(
        serializers.serialize("json", Activities_Inputs.objects.all()),
        content_type="application/json",
    )


def index(request):
    template_url = "activities_inputs/index.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ACTIVITIES_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    search_form = ActivitiesInputsSearchIndexForm(request.POST or None)
    if request.method == "POST" and search_form.is_valid():
        display_search = True
    else:
        display_search = False

    table = ActivitiesInputsTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ACTIVITIES,
            "title": "Activities Inputs",
            "activity_name": "Activities Inputs",
            "user": user,
            "auth_permissions": auth_permissions,
            "table": table,
            "search_form": search_form,
            "display_search": display_search,
            "index_url": reverse("activities_index"),
            "select_multiple_url": reverse("activities_inputs_select_multiple"),
        },
    )


@csrf_exempt
def select_single(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    action = request.POST["action"]
    id = request.POST["id"]
    comments = request.POST.get("comments")

    if action == "" or id is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    try:
        model = Activities_Inputs.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, Activities_Inputs.DoesNotExist):
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    try:
        activity = Activities.objects.get(activity_id=model.activity_id)
    except (TypeError, ValueError, OverflowError, Activities.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        project = Projects.objects.get(project_id=activity.project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    if action == "budget accept":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_ACCEPT
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if (
            model.activity_input_status == model.STATUS_DRAFT
            or model.activity_input_status == model.STATUS_BUDGET_DENIED
            or model.activity_input_status == model.STATUS_BUDGET_REJECTED
        ):
            Methods_Activities_Inputs.update_status(
                request,
                user,
                model,
                model.STATUS_BUDGET_ACCEPTED,
                project.project_assigned_to,
                comments,
            )
            messages.success(request, "Budget accepted successfully.")

    if action == "expenses accept":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_ACCEPT
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if (
            model.activity_input_status == model.STATUS_DRAFT
            or model.activity_input_status == model.STATUS_BUDGET_ACCEPTED
            or model.activity_input_status == model.STATUS_EXPENSES_DENIED
        ):
            Methods_Activities_Inputs.update_status(
                request,
                user,
                model,
                model.STATUS_EXPENSES_ACCEPTED,
                project.project_assigned_to,
                comments,
            )
            messages.success(request, "Expenses accepted successfully.")

    if action == "budget reject":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_REJECT
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")

        Methods_Activities_Inputs.update_status(
            request,
            user,
            model,
            model.STATUS_BUDGET_REJECTED,
            project.project_assigned_to,
            comments,
        )
        messages.success(request, "Budget rejected successfully.")

    if action == "expenses reject":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_REJECT
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        Methods_Activities_Inputs.update_status(
            request,
            user,
            model,
            model.STATUS_EXPENSES_REJECTED,
            project.project_assigned_to,
            comments,
        )
        messages.success(request, "Expenditure rejected successfully.")

    if action == "budget approve":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_APPROVE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if model.activity_input_status == model.STATUS_BUDGET_ACCEPTED:
            Methods_Activities_Inputs.update_status(
                request,
                user,
                model,
                model.STATUS_BUDGET_APPROVED,
                project.project_created_by,
                comments,
            )
            messages.success(request, "Budget approved successfully.")

    if action == "expenses approve":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_APPROVE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if model.activity_input_status == model.STATUS_EXPENSES_ACCEPTED:
            Methods_Activities_Inputs.update_status(
                request,
                user,
                model,
                model.STATUS_EXPENSES_APPROVED,
                project.project_created_by,
                comments,
            )
            messages.success(request, "Expenditure approved successfully.")

    if action == "budget deny":
        if settings.ACCESS_PERMISSION_ACTIVITIES_DENY not in auth_permissions.values():
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if model.activity_input_status == model.STATUS_BUDGET_ACCEPTED:
            Methods_Activities_Inputs.update_status(
                request,
                user,
                model,
                model.STATUS_BUDGET_DENIED,
                project.project_created_by,
                comments,
            )
            messages.success(request, "Budget denied successfully.")

    if action == "expenses deny":
        if settings.ACCESS_PERMISSION_ACTIVITIES_DENY not in auth_permissions.values():
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if model.activity_input_status == model.STATUS_EXPENSES_ACCEPTED:
            Methods_Activities_Inputs.update_status(
                request,
                user,
                model,
                model.STATUS_EXPENSES_DENIED,
                project.project_created_by,
                comments,
            )
            messages.success(request, "Expenses denied successfully.")

    if action == "double_count_yes":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_APPROVE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if model.activity_input_double_count == 0:
            Methods_Activities_Inputs.update_double_count(request, user, model, 1)
            messages.success(request, "Double Count is Yes.")

    if action == "double_count_no":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_APPROVE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if model.activity_input_double_count == 1:
            Methods_Activities_Inputs.update_double_count(request, user, model, 0)
            messages.success(request, "Double Count is No.")

    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        Methods_Activities_Inputs.delete(request, user, model)
        messages.success(request, "Deleted successfully.")

    Methods_Activities.update_status(request, user, activity, action)
    return HttpResponse("success", content_type="text/plain")


@csrf_exempt
def select_multiple(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ACTIVITIES_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    action = request.POST["action"]
    ids = request.POST["ids"]
    try:
        ids = ids.split(",")
    except (TypeError, ValueError, OverflowError):
        ids = None
    if action == "" or ids is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    if action == "double_count_yes":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_APPROVE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        for id in ids:
            try:
                model = Activities_Inputs.objects.get(pk=id)
                Methods_Activities_Inputs.update_double_count(request, user, model, 1)
            except (
                TypeError,
                ValueError,
                OverflowError,
                Activities_Inputs.DoesNotExist,
            ):
                continue
        messages.success(request, "Double Count is Yes to selected inputs.")

    if action == "double_count_no":

        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_APPROVE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        for id in ids:
            try:
                model = Activities_Inputs.objects.get(pk=id)
                Methods_Activities_Inputs.update_double_count(request, user, model, 0)
            except (
                TypeError,
                ValueError,
                OverflowError,
                Activities_Inputs.DoesNotExist,
            ):
                continue
        messages.success(request, "Double Count is No to selected inputs.")

    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        for id in ids:
            try:
                model = Activities_Inputs.objects.get(pk=id)
                Methods_Activities_Inputs.delete(request, user, model)
            except (
                TypeError,
                ValueError,
                OverflowError,
                Activities_Inputs.DoesNotExist,
            ):
                continue
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")


def create(request, activity_id):
    template_url = "activities_inputs/create.html"
    double_count = 0
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ACTIVITIES_CREATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    try:
        activity = Activities.objects.get(pk=activity_id)

    except (TypeError, ValueError, OverflowError, Activities.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        project = Projects.objects.get(project_id=activity.project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        organization = Organizations.objects.get(
            organization_id=project.organization_id
        )
        org_level = Levels.objects.get(level_id=organization.organization_type)
        
        organization = Methods_Organizations.format_view(request, user, organization)
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    

    if request.method == "POST":
        form = ActivitiesInputsCreateForm(
            request.POST, user=user, project_id=project.pk
        )
        if form.is_valid():
            transfer_level = Levels.objects.get(
                level_id=form.cleaned_data["transfer_class"]
            )
            transfer_code = transfer_level.level_code.strip()
            if org_level.level_code in DOUBLE_COUNT_ORG_TYPE and transfer_code in DOUBLE_COUNT_TRANSFER:
                double_count = 1
                
            sub_transfer = Levels.objects.get(
                level_id=form.cleaned_data["sub_transfer_class"]
            )
            sub_transfer_code = sub_transfer.level_code.strip()
            
            if org_level.level_code == 4 and sub_transfer_code in DOUBLE_COUNT_SUB_TRANSFER:
                double_count = 1

            data = {
                # "organization_id": project.organization_id,
                # "project_id": project.project_id,
                "activity_id": activity.activity_id,
                "input_class": form.cleaned_data["input_class"],
                "input_sub_class": form.cleaned_data["input_sub_class"],
                "scheme_class": form.cleaned_data["scheme_class"],
                "scheme_sub_class": form.cleaned_data["scheme_sub_class"],
                "funder": form.cleaned_data["funder"],
                "transfer_class": form.cleaned_data["transfer_class"],
                "sub_transfer_class": form.cleaned_data["sub_transfer_class"],
                "implementer": form.cleaned_data["implementer"],
                "division": form.cleaned_data["division"],
                "budget": form.cleaned_data["budget"],
                "budget_currency": form.cleaned_data["budget_currency"],
                "double_count": double_count,
            }
            err, msg, model = Methods_Activities_Inputs.create(request, user, data)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_ACTIVITIES,
                        "title": "Activities_Inputs",
                        "name": "Activities_Inputs",
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                        "activity": activity,
                        "organization": organization,
                    },
                )
            messages.success(request, "Created successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_ACTIVITIES,
                    model.activity_id,
                    "Created activities_inputs.",
                    user.user_id,
                    user.user_name,
                )
            )

            #     return JsonResponse({'activity_id': model.activity_id, 'message':"success"})
            # else:
            #     return HttpResponse(str(form.errors), content_type="text/plain")
            return redirect(reverse("activities_view", args=[model.activity_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_ACTIVITIES,
                    "title": "Activities Inputs",
                    "name": "Activities Inputs",
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                },
            )

    form = ActivitiesInputsCreateForm(user=user, project_id=project.pk)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ACTIVITIES,
            "title": "Activities Inputs",
            "name": "Activities Inputs",
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "activity": activity,
            "organization": organization,
        },
    )


def update(request, pk):
    template_url = "activities_inputs/update.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ACTIVITIES_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Activities_Inputs.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Activities_Inputs.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        activity = Activities.objects.get(pk=model.activity_id)
    except (TypeError, ValueError, OverflowError, Activities.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        project = Projects.objects.get(project_id=activity.project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        organization = Organizations.objects.get(
            organization_id=project.organization_id
        )
        organization = Methods_Organizations.format_view(request, user, organization)
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    if request.method == "POST":
        form = ActivitiesInputsUpdateForm(
            request.POST, user=user, project_id=project.pk
        )
        if form.is_valid():
            data = {
                "activity_id": activity.activity_id,
                "input_class": form.cleaned_data["input_class"],
                "input_sub_class": form.cleaned_data["input_sub_class"],
                "scheme_class": form.cleaned_data["scheme_class"],
                "scheme_sub_class": form.cleaned_data["scheme_sub_class"],
                "funder": form.cleaned_data["funder"],
                "transfer_class": form.cleaned_data["transfer_class"],
                "sub_transfer_class": form.cleaned_data["sub_transfer_class"],
                "implementer": form.cleaned_data["implementer"],
                "division": form.cleaned_data["division"],
                "budget": form.cleaned_data["budget"],
                "budget_currency": form.cleaned_data["budget_currency"],
            }
            err, msg, model = Methods_Activities_Inputs.update(
                request, user, data, model
            )
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_ACTIVITIES,
                        "title": "Activities Inputs",
                        "name": "Activities Inputs",
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                        "model": model,
                        "activity": activity,
                        "organization": organization,
                    },
                )
            messages.success(request, "Updated successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_ACTIVITIES,
                    model.activity_id,
                    "Updated activities_inputs.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("activities_view", args=[model.activity_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_ACTIVITIES,
                    "title": "Activities Inputs",
                    "name": "Activities Inputs",
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "model": model,
                    "activity": activity,
                    "organization": organization,
                },
            )

    form = ActivitiesInputsUpdateForm(
        user=user,
        initial=Methods_Activities_Inputs.form_view(request, user, model),
        project_id=project.pk,
    )
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ACTIVITIES,
            "title": "Activities Inputs",
            "name": "Activities Inputs",
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "model": model,
            "activity": activity,
            "organization": organization,
        },
    )


def view(request, pk):
    template_url = "activities_inputs/view.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_PROJECTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Activities_Inputs.objects.get(pk=pk)
        budget = model.activity_input_budget
        expenditure = model.activity_input_expenses
    except (TypeError, ValueError, OverflowError, Activities_Inputs.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        activity = Activities.objects.get(activity_id=model.activity_id)
    except (TypeError, ValueError, OverflowError, Activities.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        project = Projects.objects.get(project_id=activity.project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        organization = Organizations.objects.get(
            organization_id=project.organization_id
        )
        organization = Methods_Organizations.format_view(request, user, organization)
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    model = Methods_Activities_Inputs.format_view(request, user, model)
    form = ActivitiesInputsViewForm(
        user=user,
        initial=Methods_Activities_Inputs.form_view(request, user, model),
        project_id=project.pk,
    )

    count_logs = Methods_Mongo.get_collection(settings.MODEL_LOGS).count_documents(
        {"model": "activities_inputs", "modelId": model.activity_id}
    )
    form_comments = CommentsCreateForm(user=None)
    table = ActivitiesInputsTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ACTIVITIES,
            "title": "Activities Inputs",
            "name": "Activities Inputs",
            "user": user,
            "auth_permissions": auth_permissions,
            "budget": budget,
            "expenditure": expenditure,
            "model": model,
            "form": form,
            "activity": activity,
            "organization": organization,
            "form_comments": form_comments,
            "index_url": reverse("activities_inputs_index"),
            "select_single_url": reverse("activities_inputs_select_single"),
            "select_multiple_url": reverse("activities_inputs_select_multiple"),
            "table": table,
            "count_logs": count_logs,
        },
    )


def add_expenditure(request, pk):
    template_url = "activities_inputs/expenditure.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ACTIVITIES_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Activities_Inputs.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Activities_Inputs.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        activity = Activities.objects.get(pk=model.activity_id)
    except (TypeError, ValueError, OverflowError, Activities.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    if request.method == "POST":
        form = ActivitiesInputsExpenditureForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "input_class": form.cleaned_data["input_class"],
                "input_sub_class": form.cleaned_data["input_sub_class"],
                "scheme_class": form.cleaned_data["scheme_class"],
                "scheme_sub_class": form.cleaned_data["scheme_sub_class"],
                "funder": form.cleaned_data["funder"],
                "transfer_class": form.cleaned_data["transfer_class"],
                "sub_transfer_class": form.cleaned_data["sub_transfer_class"],
                "implementer": form.cleaned_data["implementer"],
                "division": form.cleaned_data["division"],
                "budget": form.cleaned_data["budget"],
                "budget_currency": form.cleaned_data["budget_currency"],
                "expenses": form.cleaned_data["expenses"],
                "expenses_currency": form.cleaned_data["expenses_currency"],
                # "fiscal_year": form.cleaned_data["fiscal_year"],
            }
            err, msg, model = Methods_Activities_Inputs.update(
                request, user, data, model
            )
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_ACTIVITIES,
                        "title": "Activities Inputs",
                        "name": "Activities Inputs",
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                        "model": model,
                        "activity": activity,
                    },
                )
            messages.success(request, "Added Expenditure successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_ACTIVITIES,
                    model.activity_id,
                    "Added axpenditure on activities_inputs.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("activities_view", args=[model.activity_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_ACTIVITIES,
                    "title": "Activities Inputs",
                    "name": "Activities Inputs",
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "model": model,
                    "activity": activity,
                },
            )

    form = ActivitiesInputsExpenditureForm(
        user=user, initial=Methods_Activities_Inputs.form_view(request, user, model)
    )
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ACTIVITIES,
            "title": "Activities Inputs",
            "name": "Activities Inputs",
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "model": model,
            "activity": activity,
        },
    )
