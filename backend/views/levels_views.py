import asyncio
import json

from django.contrib import messages
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from app import settings
from app.models.levels import Levels
from app.models.methods.levels import Methods_Levels
from app.models.methods.logs import Methods_Logs
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.status import Methods_Status
from app.models.methods.users import Methods_Users
from app.models.organizations import Organizations
from app.models.reports import Reports
from app.models.users import Users
#from backend.forms.divisions_forms import DivisionsSearchIndexForm
from backend.forms.levels_forms import (LevelsCreateForm,
                                        LevelsSearchIndexForm,
                                        LevelsUpdateForm, LevelsViewForm)
#from backend.tables.divisions_tables import DivisionsTable
from backend.tables.levels_tables import LevelsTable


class AjaxLevelsList(View):
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

        column1 = "level_code"
        column2 = "level_name"
        column3 = "level_parent"
        column4 = "level_key"
        # column4 = "level_updated_at"
        # column5 = "level_updated_by"
        # column6 = "level_status"

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
        objects = Levels.objects

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

        objects_filter = False
        if search:
            objects_filter = True
            filter_parent = Levels.objects.filter(
                Q(level_code__icontains=search)
                | Q(level_name__icontains=search)
            )
            # filter_users = Users.objects.filter(Q(user_name__icontains=search))
            objects = objects.filter(
                Q(level_code__icontains=search)
                | Q(level_name__icontains=search)
                | Q(level_parent__in=filter_parent)
                | Q(level_key__icontains=search)
                # | Q(level_updated_by__in=filter_users)
            )

        column_index = 1
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            objects = objects.filter(Q(level_code__icontains=column_search))

        column_index = 2
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            objects = objects.filter(Q(level_name__icontains=column_search))

        column_index = 3
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            filter_parent = Levels.objects.filter(
                Q(level_code__icontains=column_search)
                | Q(level_name__icontains=column_search)
            )
            objects = objects.filter(Q(level_parent__in=filter_parent))
        
        column_index = 4
        column_search = datatables.get(
            "columns[" + str(column_index) + "][search][value]"
        )
        if column_search != "":
            objects_filter = True
            objects = objects.filter(Q(level_key__icontains=column_search))

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
            row_number = LevelsTable.render_row_number(record, counter)
            value1 = LevelsTable.render_level_code(record)
            value2 = LevelsTable.render_level_name(record)
            value3 = LevelsTable.render_level_parent(record)
            value4 = LevelsTable.render_level_key(record)
            actions = LevelsTable.render_actions(record, auth_permissions)

            data.append(
                {
                    "row_number": row_number,
                    "level_code": value1,
                    "level_name": value2,
                    "level_parent": value3,
                    "level_key": value4,
                    "actions": actions,
                }
            )

        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }


def json_levels(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_LEVELS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    return HttpResponse(
        serializers.serialize("json", Levels.objects.all()),
        content_type="application/json",
    )


def index(request):
    template_url = "levels/index.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_LEVELS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    search_form = LevelsSearchIndexForm(request.POST or None)
    if request.method == "POST" and search_form.is_valid():
        display_search = True
    else:
        display_search = False

    table = LevelsTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_LEVELS,
            "title": Levels.TITLE,
            "name": Levels.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "table": table,
            "search_form": search_form,
            "display_search": display_search,
            "index_url": reverse("levels_index"),
            "select_multiple_url": reverse("levels_select_multiple"),
        },
    )


@csrf_exempt
def select_single(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_LEVELS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    action = request.POST["action"]
    id = request.POST["id"]
    if action == "" or id is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    try:
        model = Levels.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    if action == "block":
        if model.level_status == Methods_Status.STATUS_ACTIVE:
            Methods_Levels.update_status(
                request, user, model, Methods_Status.STATUS_BLOCKED
            )
            messages.success(request, "Blocked successfully.")

    if action == "unblock":
        if model.level_status == Methods_Status.STATUS_BLOCKED:
            Methods_Levels.update_status(
                request, user, model, Methods_Status.STATUS_ACTIVE
            )
            messages.success(request, "Unblocked successfully.")

    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_LEVELS_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        Methods_Levels.delete(request, user, model)
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")


@csrf_exempt
def select_multiple(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_LEVELS_UPDATE not in auth_permissions.values():
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
                model = Levels.objects.get(pk=id)
                if model.level_status == Methods_Status.STATUS_ACTIVE:
                    Methods_Levels.update_status(
                        request, user, model, Methods_Status.STATUS_BLOCKED
                    )
            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                continue
        messages.success(request, "Blocked successfully.")

    if action == "unblock":
        for id in ids:
            try:
                model = Levels.objects.get(pk=id)
                if model.level_status == Methods_Status.STATUS_BLOCKED:
                    Methods_Levels.update_status(
                        request, user, model, Methods_Status.STATUS_INACTIVE
                    )
            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                continue
        messages.success(request, "Unblocked successfully.")

    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_LEVELS_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        for id in ids:
            try:
                model = Levels.objects.get(pk=id)
                Methods_Levels.delete(request, user, model)
            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                continue
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")


def create(request):
    template_url = "levels/create.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_LEVELS_CREATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")


    if request.method == "POST":
        form = LevelsCreateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "key": form.cleaned_data["key"],
                "code": form.cleaned_data["code"],
                "name": form.cleaned_data["name"],
                "parent": form.cleaned_data["parent"],
            }
            err, msg, model = Methods_Levels.create(request, user, data)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_LEVELS,
                        "title": Levels.TITLE,
                        "name": Levels.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                    },
                )
            messages.success(request, "Created successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_LEVELS,
                    model.level_id,
                    "Created levels.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("levels_view", args=[model.level_id]))

        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_LEVELS,
                    "title": Levels.TITLE,
                    "name": Levels.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                },
            )

    form = LevelsCreateForm(user=user)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_LEVELS,
            "title": Levels.TITLE,
            "name": Levels.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
        },
    )


def update(request, pk):
    template_url = "levels/update.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_LEVELS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Levels.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    if request.method == "POST":
        form = LevelsUpdateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "key": form.cleaned_data["key"],
                "code": form.cleaned_data["code"],
                "name": form.cleaned_data["name"],
                "parent": form.cleaned_data["parent"],
            }
            err, msg, model = Methods_Levels.update(request, user, data, model)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_LEVELS,
                        "title": Levels.TITLE,
                        "name": Levels.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                        "model": model,
                    },
                )
            messages.success(request, "Updated successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_LEVELS,
                    model.level_id,
                    "Updated levels.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("levels_view", args=[model.level_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_LEVELS,
                    "title": Levels.TITLE,
                    "name": Levels.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "model": model,
                },
            )

    form = LevelsUpdateForm(
        user=user, initial=Methods_Levels.form_view(request, user, model)
    )
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_LEVELS,
            "title": Levels.TITLE,
            "name": Levels.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "model": model,
        },
    )


def view(request, pk):
    template_url = "levels/view.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_LEVELS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Levels.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    model = Methods_Levels.format_view(request, user, model)
    form = LevelsViewForm(
        user=user, initial=Methods_Levels.form_view(request, user, model)
    )
    count_logs = Methods_Mongo.get_collection(settings.MODEL_LOGS).count_documents(
        {"model": "levels", "modelId": model.level_id}
    )

    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_LEVELS,
            "title": Levels.TITLE,
            "name": Levels.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "model": model,
            "form": form,
            "index_url": reverse("levels_index"),
            "select_single_url": reverse("levels_select_single"),
            "count_logs": count_logs,
        },
    )


def dropdown(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    Methods_Users.get_auth_permissions(user)
    values = "<option value='0' selected>NONE</option>"
    levels = Levels.objects.order_by("level_code").all()
    for level in levels:
        values += (
            "<option value='"
            + str(level.level_id)
            + "'>"
            + str(level.level_code) + ': ' + str(level.level_name)
            + "</option>"
        )

    return HttpResponse(values, content_type="text/plain")

def type_status_dropdown(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    Methods_Users.get_auth_permissions(user)
    values = "<option value='0' selected>--Select--</option>"
    level_parent = request.GET.get("level_parent")
    level_key = request.GET.get("level_key")
    levels = Levels.objects.filter(level_parent=level_parent,level_key = level_key ).order_by("level_code")
    for level in levels:
        values += (
            "<option value='"
            + str(level.level_id)
            + "'>"
            + str(level.level_code) + ': ' + str(level.level_name)
            + "</option>"
        )

    return HttpResponse(values, content_type="text/plain")



def tree(request, pk):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    Methods_Users.get_auth_permissions(user)
    values = Methods_Levels.tree(request, user, pk)
    return HttpResponse(values, content_type="text/plain")

def tree_create(request, key,model):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    Methods_Users.get_auth_permissions(user)
    values = ''
    items = None
    if model == 'reports' or model == 'organizations':
        items = Levels.objects.filter(
        Q(level_key=key) &
        Q(level_parent=0)
    ).all()
    for item in items:
        values += Methods_Levels.tree_create(request, user, item.level_id)
    return HttpResponse(values, content_type="text/plain")



def tree_edit(request, key, model, model_id):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    Methods_Users.get_auth_permissions(user)
    values = ''

    selected = []
    if model == 'organizations':
        try:
            organization = Organizations.objects.get(pk=model_id)
            if key == 'financing-source-type':
                selected = organization.organization_financial_sources_class
            # if key == 'organization-status':
            #     selected = organization.organization_levels_status
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            return HttpResponseNotFound("Not Found", content_type="text/plain")

    if model == 'reports':
        try:
            report = Reports.objects.get(pk=model_id)
            if key == 'financing-source-type':
                selected = report.report_funds_transfer_class
        except (TypeError, ValueError, OverflowError, Reports.DoesNotExist):
            return HttpResponseNotFound("Not Found", content_type="text/plain")

    items = Levels.objects.filter(
        Q(level_key=key) &
        Q(level_parent=0)
    ).all()
    for item in items:
        values += Methods_Levels.tree_edit(request, user, item.level_id, selected)
    return HttpResponse(values, content_type="text/plain")

def tree_view(request, key, model, model_id):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    Methods_Users.get_auth_permissions(user)
    values = ''

    selected = []
    if model == 'organizations':
        try:
            organization = Organizations.objects.get(pk=model_id)
            if key == 'financing-source-type':
                selected = organization.organization_financial_sources_class
            # if key == 'organization-status':
            #     selected = organization.organization_levels_status
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    if model == 'reports':
        try:
            report = Reports.objects.get(pk=model_id)
            if key == 'financing-source-type':
                selected = report.report_funds_transfer_class
        except (TypeError, ValueError, OverflowError, Reports.DoesNotExist):
            return HttpResponseNotFound("Not Found", content_type="text/plain")

    items = Levels.objects.filter(
        Q(level_key=key) &
        Q(level_parent=0)
    ).all()
    for item in items:
        values += Methods_Levels.tree_view(request, user, item.level_id, selected)
    return HttpResponse(values, content_type="text/plain")