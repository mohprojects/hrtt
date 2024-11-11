import asyncio
import json

from django.contrib import messages
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound,
                         JsonResponse)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from app import settings
from app.models.methods.logs import Methods_Logs
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.organizations import Methods_Organizations
from app.models.methods.status import Methods_Status
from app.models.methods.users import Methods_Users
from app.models.methods.emails import Methods_Emails
from app.models.organizations import Organizations
from app. models.projects import Projects
from app.models.users import Users
from app.utils import Utils
from app.models.levels import Levels
from backend.forms.organizations_forms import (OrganizationsCreateForm,
                                               OrganizationsSearchIndexForm,
                                               OrganizationsUpdateForm,
                                               OrganizationsViewForm)

from backend.tables.organizations_tables import OrganizationsTable

class AjaxOrganizationsList(View):
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

        column1 = "organization_name"
        column2 = "organization_type"
        column3 = "organization_category"
        column4 = "organization_updated_at"
        column5 = "organization_updated_by"
        column6 = "organization_status"

        datatables = request.GET

        # item draw
        draw = int(datatables.get("draw"))
        # item start
        start = int(datatables.get("start"))
        # item length (limit)
        length = int(datatables.get("length"))
        # item data search
        search = datatables.get("search[value]")

        # Get objects
        objects = Organizations.objects

        # Set record total
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
                Q(organization_name__icontains=search)
                | Q(organization_type__icontains=search)
                | Q(organization_category__icontains=search)
                | Q(organization_updated_by__in=filter_users)
            )

        column_index = 1
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            objects = objects.filter(Q(organization_name__icontains=column_search))

        column_index = 2
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            filter_levels = Levels.objects.filter(Q(level_name__icontains=column_search))
            objects = objects.filter(Q(organization_type__in=filter_levels))

        column_index = 3
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            objects = objects.filter(Q(organization_category__icontains=column_search))

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
                Q(organization_updated_at__gte=seconds)
                & Q(organization_updated_at__lt=(seconds + 86400))
            )

        column_index = 5
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            filter_users = Users.objects.filter(Q(user_name__icontains=column_search))
            objects = objects.filter(Q(organization_updated_by__in=filter_users))

        column_index = 6
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            objects = objects.filter(
                Q(
                    organization_status=Organizations.ARRAY_TEXT_STATUS.index(
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
            row_number = OrganizationsTable.render_row_number(record, counter)
            value1 = OrganizationsTable.render_organization_name(record)
            value2 = OrganizationsTable.render_organization_type(record)
            value3 = OrganizationsTable.render_organization_category(record)
            value4 = OrganizationsTable.render_organization_updated_at(record)
            value5 = OrganizationsTable.render_organization_updated_by(record)
            value6 = OrganizationsTable.render_organization_status(record)
            actions = OrganizationsTable.render_actions(record, auth_permissions)

            data.append(
                {
                    "row_number": row_number,
                    "organization_name": value1,
                    "organization_type": value2,
                    "organization_category": value3,
                    "organization_updated_at": value4,
                    "organization_updated_by": value5,
                    "organization_status": value6,
                    "actions": actions,
                }
            )


        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }


def json_organizations(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    return HttpResponse(
        serializers.serialize("json", Organizations.objects.all()),
        content_type="application/json",
    )


def index(request):
    template_url = "organizations/index.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    search_form = OrganizationsSearchIndexForm(request.POST or None)
    if request.method == "POST" and search_form.is_valid():
        display_search = True
    else:
        display_search = False

    table = OrganizationsTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ORGANIZATIONS,
            "title": Organizations.TITLE,
            "name": Organizations.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "table": table,
            "search_form": search_form,
            "display_search": display_search,
            "index_url": reverse("organizations_index"),
            "select_multiple_url": reverse("organizations_select_multiple"),
        },
    )


@csrf_exempt
def select_single(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    action = request.POST["action"]
    id = request.POST["id"]
    if action == "" or id is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    try:
        model = Organizations.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    if action == "block":
        if model.organization_status ==  model.STATUS_ACTIVE:
            Methods_Organizations.update_status(
                request, user, model,  model.STATUS_INNACTIVE
            )
            messages.success(request, "Deactivated successfully.")

    if action == "unblock":
        if model.organization_status ==  model.STATUS_INNACTIVE:
            Methods_Organizations.update_status(
                request, user, model,  model.STATUS_ACTIVE
            )
            messages.success(request, "Activated successfully.")

    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_ORGANIZATIONS_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        Methods_Organizations.delete(request, user, model)
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")


@csrf_exempt
def select_multiple(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE not in auth_permissions.values():
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
                model = Organizations.objects.get(pk=id)
                if model.organization_status == Methods_Status.STATUS_ACTIVE:
                    Methods_Organizations.update_status(
                        request, user, model, Methods_Status.STATUS_BLOCKED
                    )
            except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                continue
        messages.success(request, "Blocked successfully.")

    if action == "unblock":
        for id in ids:
            try:
                model = Organizations.objects.get(pk=id)
                if model.organization_status == Methods_Status.STATUS_BLOCKED:
                    Methods_Organizations.update_status(
                        request, user, model, Methods_Status.STATUS_INACTIVE
                    )
            except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                continue
        messages.success(request, "Unblocked successfully.")

    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_ORGANIZATIONS_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        for id in ids:
            try:
                model = Organizations.objects.get(pk=id)
                Methods_Organizations.delete(request, user, model)
            except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                continue
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")


def create(request):
    template_url = "organizations/create.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_CREATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    if request.method == "POST":
        form = OrganizationsCreateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
                "phone_number": form.cleaned_data["phone_number"],
                "email": form.cleaned_data["email"],
                "type": form.cleaned_data["type"],
                "category": form.cleaned_data["category"],
                "financial_agent_class": form.cleaned_data["financial_agent_class"],
                "financial_agent_sub_class": form.cleaned_data["financial_agent_sub_class"],
                "financial_schemes_name": form.cleaned_data["financial_schemes_name"],
                "financial_schemes_class": form.cleaned_data["financial_schemes_class"],
                "financial_schemes_sub_class": form.cleaned_data["financial_schemes_sub_class"],
                "healthcare_class": form.cleaned_data["healthcare_class"],
                "healthcare_sub_class": form.cleaned_data["healthcare_sub_class"],
                "sub_type": form.cleaned_data['sub_type'],
            }
           
            err, msg, model = Methods_Organizations.create(request, user, data)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_ORGANIZATIONS,
                        "title": Organizations.TITLE,
                        "name": Organizations.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                    },
                )
           
            Methods_Emails.send_info_email(
                request,
                model.organization_email,
                "Dear Sir/Madam",
                "Your Organization has been successfully created on HRTT.",
            )
            messages.success(request, "Created successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_ORGANIZATIONS,
                    model.organization_id,
                    "Created organizations.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("organizations_view", args=[model.organization_id]))

        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_ORGANIZATIONS,
                    "title": Organizations.TITLE,
                    "name": Organizations.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                },
            )

    form = OrganizationsCreateForm(user=user)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ORGANIZATIONS,
            "title": Organizations.TITLE,
            "name": Organizations.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
        },
    )


def update(request, pk):
    template_url = "organizations/update.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Organizations.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    if request.method == "POST":
        form = OrganizationsUpdateForm(request.POST, user=user)
        financial_data = request.POST.get("financing_source")
        if form.is_valid():
            data = {
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
                "phone_number": form.cleaned_data["phone_number"],
                "email": form.cleaned_data["email"],
                "type": form.cleaned_data["type"],
                "category": form.cleaned_data["category"],
                "financial_agent_class": form.cleaned_data["financial_agent_class"],
                "financial_agent_sub_class": form.cleaned_data["financial_agent_sub_class"],
                "financial_schemes_name": form.cleaned_data["financial_schemes_name"],
                "financial_schemes_class": form.cleaned_data["financial_schemes_class"],
                "financial_schemes_sub_class": form.cleaned_data["financial_schemes_sub_class"],
                "healthcare_class": form.cleaned_data["healthcare_class"],
                "healthcare_sub_class": form.cleaned_data["healthcare_sub_class"],
                "sub_type": form.cleaned_data['sub_type'],
            }
            if financial_data is not None:
                data.update({"financial_sources_class":financial_data})
                err, msg, model = Methods_Organizations.update(request, user, data, model)
            else: 
                err, msg, model = Methods_Organizations.update(request, user, data, model)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_ORGANIZATIONS,
                        "title": Organizations.TITLE,
                        "name": Organizations.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                        "model": model,
                    },
                )
            
            messages.success(request, "Updated successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_ORGANIZATIONS,
                    model.organization_id,
                    "Updated organizations.",
                    user.user_id,
                    user.user_name,
                )
            )
            #return redirect(reverse("organizations_view", args=[model.organization_id]))
            return JsonResponse({'organization_id': model.organization_id, 'message':"success"})
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_ORGANIZATIONS,
                    "title": Organizations.TITLE,
                    "name": Organizations.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "model": model,
                },
            )

    form = OrganizationsUpdateForm(
        user=user, initial=Methods_Organizations.form_view(request, user, model)
    )
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ORGANIZATIONS,
            "title": Organizations.TITLE,
            "name": Organizations.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "model": model,
        },
    )


def view(request, pk):
    template_url = "organizations/view.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Organizations.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    try:
        tags_in_Projects = Projects.objects.filter(Q(project_tags__icontains = model.organization_id))
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    model = Methods_Organizations.format_view(request, user, model)
    form = OrganizationsViewForm(
        user=user, initial=Methods_Organizations.form_view(request, user, model)
    )
    count_logs = Methods_Mongo.get_collection(settings.MODEL_LOGS).count_documents(
        {"model": "organizations", "modelId": model.organization_id}
    )

    # search_form_divisions = DivisionsSearchIndexForm(request.POST or None)
    # if request.method == "POST" and search_form_divisions.is_valid():
    #     display_search_divisions = True
    # else:
    #     display_search_divisions = False
    # table_divisions = DivisionsTable({})
    # # table.paginate(page=request.GET.get('page', 1), per_page=5)
    # table_divisions.set_auth_permissions(auth_permissions)

    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ORGANIZATION,
            "title": Organizations.TITLE,
            "name": Organizations.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "model": model,
            "form": form,
            "tags_in_Projects":tags_in_Projects,
            "index_url": reverse("organizations_index"),
            "select_single_url": reverse("organizations_select_single"),
            "count_logs": count_logs,
            # "table_divisions": table_divisions,
            # "search_form": search_form_divisions,
            # "display_search": display_search_divisions,
            #"select_multiple_url_divisions": reverse("divisions_select_multiple"),
        },
    )


def dropdown(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    Methods_Users.get_auth_permissions(user)
    values = "<option value='0' selected>NONE</option>"
    request.GET
    organizations = Organizations.objects.order_by("organization_name").all()
    for organization in organizations:
        values += (
            "<option value='"
            + str(organization.organization_id)
            + "'>"
            + str(organization.organization_name)
            + "</option>"
        )

    return HttpResponse(values, content_type="text/plain")


def update_levels_type(request, pk):
    template_url = "organizations/update-levels-type.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Organizations.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ORGANIZATIONS,
            "title": Organizations.TITLE,
            "name": Organizations.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "model": model,
        },
    )

@csrf_exempt
def update_levels_type_submit(request, pk):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Organizations.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    data = request.POST['selected']
    model = Methods_Organizations.update_levels_type(request, user, model, data)
    return HttpResponse("success", content_type="text/plain")


def update_levels_status(request, pk):
    template_url = "organizations/update-levels-status.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Organizations.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ORGANIZATIONS,
            "title": Organizations.TITLE,
            "name": Organizations.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "model": model,
        },
    )

@csrf_exempt
def update_levels_status_submit(request, pk):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Organizations.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    data = request.POST['selected']
    model = Methods_Organizations.update_levels_status(request, user, model, data)
    return HttpResponse("success", content_type="text/plain")
