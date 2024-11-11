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
from app.models.activities import Activities
from app.models.levels import Levels
from app.models.methods.activities import Methods_Activities
from app.models.methods.projects import Methods_Projects
from app.models.methods.logs import Methods_Logs
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.users import Methods_Users

from app.models.users import Users
from app.models.projects import Projects
from app.models.activities_inputs import Activities_Inputs
from app.utils import Utils
from backend.forms.activities_forms import (
    ActivitiesCreateForm,
    ActivitiesSearchIndexForm,
    ActivitiesUpdateForm,
    ActivitiesViewForm,
)
from backend.forms.comments_forms import (
    CommentsCreateForm,
    CommentsCreateHtmlForm,
   
)
from backend.forms.activities_inputs_forms import ActivitiesInputsSearchIndexForm
from backend.tables.activities_tables import ActivitiesTable
from backend.tables.activities_inputs_tables import ActivitiesInputsTable


class AjaxActivitiesList(View):
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
        column1 = "activity_name"
        column2 = "project_id"
        column3 = "activity_location"
        column4 = "activity_fiscal_year"
        column5 = "activity_updated_at"
        column6 = "activity_updated_by"
        column7 = "activity_status"

        datatables = request.GET
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
        objects = Activities.objects
        org_id = user.organization_id
        if user.user_role== user.TYPE_SUPER_ADMIN:
            objects = objects.exclude(Q(activity_status=Activities.STATUS_DRAFT))
            
        if user.user_role== user.TYPE_ACTIVITY_MANAGER:
            projects_ids = Projects.objects.values_list('project_id', flat=True).filter(Q(organization_id = org_id))
            objects = objects.filter(Q(project_id__in=set(projects_ids)))  
        if user.user_role== user.TYPE_DATA_REPORTER:
            projects_ids = Projects.objects.values_list('project_id', flat=True).filter(Q(organization_id = org_id) & Q(project_assigned_to = user.user_id))
            objects = objects.filter(Q(project_id__in=set(projects_ids))) 
         
        
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
            row_number = ActivitiesTable.render_row_number(record, counter)
            value1 = ActivitiesTable.render_activity_name(record)
            value2 = ActivitiesTable.render_activity_location(record)
            value4 = ActivitiesTable.render_activity_updated_at(record)
            value5 = ActivitiesTable.render_activity_updated_by(record)
            value6 = ActivitiesTable.render_activity_status(record)
            value8 = ActivitiesTable.render_activity_project(record)
            value9 = ActivitiesTable.render_activity_fy(record)
            actions = ActivitiesTable.render_actions(record, auth_permissions)

            data.append(
                {
                    "row_number": row_number,
                    "activity_name": value1,
                    "activity_location": value2,
                    "activity_updated_at": value4,
                    "activity_updated_by": value5,
                    "activity_status": value6,
                    "project_id": value8,
                    "fiscal_year": value9,
                    "actions": actions,
                }
            )

        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }


def json_activities(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ACTIVITIES_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    return HttpResponse(
        serializers.serialize("json", Activities.objects.all()),
        content_type="application/json",
    )
def table(request):
    template_url = "activities/table.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ACTIVITIES_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    search_form = ActivitiesSearchIndexForm(request.POST or None)
    if request.method == "POST" and search_form.is_valid():
        display_search = True
    else:
        display_search = False

    table = ActivitiesTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ACTIVITIES,
            "title": Activities.TITLE,
            "activity_name": Activities.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "table": table,
            "search_form": search_form,
            "display_search": display_search,
            "index_url": reverse("activities_table"),
            "select_multiple_url": reverse("activities_select_multiple"),
        },
    )


def index(request,project_id):
    template_url = "activities/index.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ACTIVITIES_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    search_form = ActivitiesSearchIndexForm(request.POST or None)
    if request.method == "POST" and search_form.is_valid():
        display_search = True
    else:
        display_search = False

    try:
        project = Projects.objects.get(pk=project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    table = ActivitiesTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ACTIVITIES,
            "title": Activities.TITLE,
            "activity_name": Activities.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "table": table,
            "search_form": search_form,
            "display_search": display_search,
            "project":project,
            "index_url": reverse("activities_index",args=[project.project_id]),
            "select_multiple_url": reverse("activities_select_multiple"),
        },
    )


@csrf_exempt
def select_single(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)

    action = request.POST['action']
    id = request.POST['id']
    comments = request.POST.get('comments')


    if action == "" or id is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    try:
        model = Activities.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, Activities.DoesNotExist):
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    
    if action == "submit":
        if (
            model.activity_status == Activities.STATUS_DRAFT
            # or model.activity_status == Activities.STATUS_REJECTED
        ): 
            activities_inputs = Activities_Inputs.objects.filter(activity_id = model.activity_id)
            if len(activities_inputs) == 0:
                return HttpResponse("inputs", content_type="text/plain")
            Methods_Activities.update_status(request, user, model,Activities.STATUS_SUBMITTED)
            project_model = Projects.objects.get(pk = model.project_id)
            if project_model.project_status == project_model.STATUS_ASSIGNED or project_model.project_status == project_model.STATUS_DRAFT:
                Methods_Projects.update_status(request,None,project_model, project_model.STATUS_ACTIVE)
            messages.success(request, "Submitted successfully.")


    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        Methods_Activities.delete(request, user, model)
        messages.success(request, "Deleted successfully.")

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

    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_ACTIVITIES_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        for id in ids:
            try:
                model = Activities.objects.get(pk=id)
                Methods_Activities.delete(request, user, model)
            except (TypeError, ValueError, OverflowError, Activities.DoesNotExist):
                continue
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")


def create(request,project_id):
    
    template_url = "activities/create.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ACTIVITIES_CREATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        project = Projects.objects.get(pk=project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    if request.method == "POST":
        form = ActivitiesCreateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "name": form.cleaned_data["name"],
                "organization_id": project.organization_id,
                "project_id": project.project_id,
                "location": form.cleaned_data["location"],
                "functions": form.cleaned_data["functions"],
                "sub_functions": form.cleaned_data["sub_functions"],
                "domain": form.cleaned_data["domain"],
                "sub_domain": form.cleaned_data["sub_domain"],
                "fiscal_year": form.cleaned_data["fiscal_year"],
            }
            err, msg, model = Methods_Activities.create(request, user,data)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_ACTIVITIES,
                        "title": Activities.TITLE,
                        "name": Activities.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                        "project":project
                    },
                )
            messages.success(request, "Saved successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_ACTIVITIES,
                    model.activity_id,
                    "Created activities.",
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
                    "title": Activities.TITLE,
                    "name": Activities.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    
                },
            )

    form = ActivitiesCreateForm(user=user)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ACTIVITIES,
            "title": Activities.TITLE,
            "name": Activities.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "project":project
        },
    )


def update(request, pk):
    template_url = "activities/update.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_ACTIVITIES_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Activities.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Activities.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        project = Projects.objects.get(pk=model.project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    if request.method == "POST":
        form = ActivitiesUpdateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "name": form.cleaned_data["name"],
                "location": form.cleaned_data["location"],
                "functions": form.cleaned_data["functions"],
                "sub_functions": form.cleaned_data["sub_functions"],
                "domain": form.cleaned_data["domain"],
                "sub_domain": form.cleaned_data["sub_domain"],
                "fiscal_year": form.cleaned_data["fiscal_year"],
               
            }
            err, msg, model = Methods_Activities.update(request, user,data, model)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_ACTIVITIES,
                        "title": Activities.TITLE,
                        "name": Activities.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                        "model": model,
                        "project": project,
                    },
                )
            messages.success(request, "Updated successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_ACTIVITIES,
                    model.activity_id,
                    "Updated activities.",
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
                    "title": Activities.TITLE,
                    "name": Activities.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "model": model,
                    "project": project,
                },
            )

    form = ActivitiesUpdateForm(
        user=user, initial=Methods_Activities.form_view(request, user, model)
    )
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_ACTIVITIES,
            "title": Activities.TITLE,
            "name": Activities.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "model": model,
            "project":project
        },
    )


def view(request, pk):
    template_url = "activities/view.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_PROJECTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Activities.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Activities.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        project = Projects.objects.get(pk=model.project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    model = Methods_Activities.format_view(request, user, model)

    form = ActivitiesViewForm(
        user=user, initial=Methods_Activities.form_view(request, user, model)
    )
    count_logs = Methods_Mongo.get_collection(settings.MODEL_LOGS).count_documents(
        {"model": "activities", "modelId": model.activity_id}
    )
    search_form_activities_inputs = ActivitiesInputsSearchIndexForm(request.POST or None)
    if request.method == "POST" and search_form_activities_inputs.is_valid():
        display_search_activities_inputs = True
    else:
        display_search_activities_inputs = False
    table_activities_inputs = ActivitiesInputsTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table_activities_inputs.set_auth_permissions(auth_permissions)

    form_comments = CommentsCreateForm(user=None)


    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_PROJECTS,
            "title": Activities.TITLE,
            "name": Activities.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "model": model,
            "project" : project,
            "form": form,
            "form_comments":form_comments,
            "table":table_activities_inputs,
            "search_form": search_form_activities_inputs,
            "display_search": display_search_activities_inputs,
            "index_url": reverse("projects_index"),
            "select_single_url": reverse("activities_select_single"),
            "select_multiple_url": reverse("activities_inputs_select_multiple"),
            "count_logs": count_logs,
        },
    )

# def get_fundings_form(request):
#     user = Users.login_required(request)
#     if user is None:
#         return HttpResponse("signin", content_type="text/plain")
#     organization_id = request.GET.get('organization_id')
#     organization = Organizations.objects.get(pk=organization_id)
#     form = FundingsCreateForm(initial={'organization': f'{organization.organization_id}: {organization.organization_name}'}, user=user)
#     return JsonResponse({'html': form.as_p()})
