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
from app.models.reports import Reports
from app.models.projects import Projects

from app.models.methods.reports import Methods_Reports
from app.models.methods.logs import Methods_Logs
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.projects import Methods_Projects
from app.models.methods.users import Methods_Users
from app.models.users import Users
from app.utils import Utils
from backend.forms.reports_forms import (
    ReportsCreateForm,
    ReportsSearchIndexForm,
    ReportsUpdateForm,
    ReportsViewForm,
)
from backend.forms.comments_forms import (
    CommentsCreateForm,
    CommentsCreateHtmlForm,
   
)
from backend.tables.reports_tables import ReportsTable


# class AjaxReportsList(View):
#     def get(self, request):
#         user = Users.login_required(request)
#         if user is None:
#             return HttpResponse(
#                 json.dumps({}, cls=DjangoJSONEncoder), content_type="application/json"
#             )
#         items = self._datatables(request, user)
#         return HttpResponse(
#             json.dumps(items, cls=DjangoJSONEncoder), content_type="application/json"
#         )

#     def _datatables(self, request, user):
#         auth_permissions = Methods_Users.get_auth_permissions(user)

#         column1 = "report_asset_name"
#         column2 = "report_purchase_value"
#         column3 = "report_year_purchased"
#         column4 = "report_updated_at"
#         column5 = "report_updated_by"
#         column6 = "report_status"

#         datatables = request.GET
#         # item draw
#         draw = int(datatables.get("draw"))
#         # item start
#         start = int(datatables.get("start"))
#         # item length (limit)
#         length = int(datatables.get("length"))
#         # item data search
#         search = datatables.get("search[value]")
#         project_id = datatables.get("project_id")

#          # Get objects
#         objects = Reports.objects.filter(Q(project_id=project_id))
#         if user.user_role== user.TYPE_ACTIVITY_MANAGER:
#             objects = objects.exclude(Q(report_status=Reports.STATUS_DRAFT))
#         if user.user_role== user.TYPE_SUPER_ADMIN:
#             objects = objects.filter(Q(report_status=Reports.STATUS_ACCEPTED)|Q(report_status=Reports.STATUS_APPROVED)| Q(report_status=Reports.STATUS_DENIED))
       
#         records_total = objects.all().count()
#         # Set records filtered
#         records_filtered = records_total

#         order_column_index = datatables.get("order[0][column]")
#         order_column_sort = datatables.get("order[0][dir]")

#         if order_column_index and order_column_sort:
#             if int(order_column_index) == 1:
#                 if order_column_sort == "asc":
#                     objects = objects.order_by(column1)
#                 if order_column_sort == "desc":
#                     objects = objects.order_by("-" + column1)
#             if int(order_column_index) == 2:
#                 if order_column_sort == "asc":
#                     objects = objects.order_by(column2)
#                 if order_column_sort == "desc":
#                     objects = objects.order_by("-" + column2)
#             if int(order_column_index) == 3:
#                 if order_column_sort == "asc":
#                     objects = objects.order_by(column3)
#                 if order_column_sort == "desc":
#                     objects = objects.order_by("-" + column3)
#             if int(order_column_index) == 4:
#                 if order_column_sort == "asc":
#                     objects = objects.order_by(column4)
#                 if order_column_sort == "desc":
#                     objects = objects.order_by("-" + column4)
#             if int(order_column_index) == 5:
#                 if order_column_sort == "asc":
#                     objects = objects.order_by(column5)
#                 if order_column_sort == "desc":
#                     objects = objects.order_by("-" + column5)
#             if int(order_column_index) == 6:
#                 if order_column_sort == "asc":
#                     objects = objects.order_by(column6)
#                 if order_column_sort == "desc":
#                     objects = objects.order_by("-" + column6)

#         objects_filter = False
#         if search:
#             objects_filter = True
#             filter_users = Users.objects.filter(Q(user_name__icontains=search))
#             objects = objects.filter(
#                 Q(report_asset_name__icontains=search)
#                 | Q(report_purchase_value__icontains=search)
#                 | Q(report_year_purchased__icontains=search)
#                 # | Q(report_status__icontains=search)
#                 | Q(report_updated_by__in=filter_users)
#             )

#         column_index = 1
#         column_search = datatables.get(
#             "columns[" + str(column_index) + "][search][value]"
#         )
#         if column_search != "":
#             objects_filter = True
#             objects = objects.filter(Q(report_asset_name__icontains=column_search))

#         column_index = 2
#         column_search = datatables.get(
#             "columns[" + str(column_index) + "][search][value]"
#         )
#         if column_search != "":
#             objects_filter = True
#             objects = objects.filter(Q(report_purchase_value__icontains=column_search))

#         column_index = 3
#         column_search = datatables.get(
#             "columns[" + str(column_index) + "][search][value]"
#         )
#         if column_search != "":
#             objects_filter = True
#             objects = objects.filter(Q(report_year_purchased__icontains=column_search))

#         column_index = 4
#         column_search = datatables.get(
#             "columns[" + str(column_index) + "][search][value]"
#         )
#         if column_search != "":
#             objects_filter = True
#             seconds = (
#                 Utils.convert_string_to_datetime(
#                     Utils.get_format_input_date(column_search) + " 00:00:00"
#                 )
#             ).timestamp() + settings.TIME_DIFFERENCE
#             objects = objects.filter(
#                 Q(report_updated_at__gte=seconds)
#                 & Q(report_updated_at__lt=(seconds + 86400))
#             )

#         column_index = 5
#         column_search = datatables.get(
#             "columns[" + str(column_index) + "][search][value]"
#         )
#         if column_search != "":
#             objects_filter = True
#             filter_users = Users.objects.filter(Q(user_name__icontains=column_search))
#             objects = objects.filter(Q(report_updated_by__in=filter_users))

#         column_index = 6
#         column_search = datatables.get(
#             "columns[" + str(column_index) + "][search][value]"
#         )
#         if column_search != "":
#             objects_filter = True
#             objects = objects.filter(
#                 Q(report_status=Reports.ARRAY_TEXT_STATUS.index(column_search))
#             )


#         if objects_filter:
#             records_filtered = objects.all().count()

#         items = objects.all()

#         if length == -1:
#             paginator = Paginator(items, items.count())
#             page_number = 1
#         else:
#             paginator = Paginator(items, length)
#             page_number = start / length + 1

#         try:
#             object_list = paginator.page(page_number).object_list
#         except PageNotAnInteger:
#             object_list = paginator.page(1).object_list
#         except EmptyPage:
#             object_list = paginator.page(1).object_list

#         counter = 0
#         data = []
#         for record in object_list:
#             counter = counter + 1
#             row_number = ReportsTable.render_row_number(record, counter)
#             value1 = ReportsTable.render_report_asset_name(record)
#             value2 = ReportsTable.render_report_purchase_value(record)
#             value3 = ReportsTable.render_report_year_purchased(record)
#             value4 = ReportsTable.render_report_updated_at(record)
#             value5 = ReportsTable.render_report_updated_by(record)
#             value6 = ReportsTable.render_report_status(record)
#             actions = ReportsTable.render_actions(record, auth_permissions)

#             data.append(
#                 {
#                     "row_number": row_number,
#                     "report_asset_name": value1,
#                     "report_purchase_value": value2,
#                     "report_year_purchased": value3,
#                     "report_updated_at": value4,
#                     "report_updated_by": value5,
#                     "report_status": value6,
#                     "actions": actions,
#                 }
#             )

#         return {
#             "draw": draw,
#             "recordsTotal": records_total,
#             "recordsFiltered": records_filtered,
#             "data": data,
#         }


def json_reports(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    return HttpResponse(
        serializers.serialize("json", Reports.objects.all()),
        content_type="application/json",
    )


def index(request,project_id):
    template_url = "reports/index.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    search_form = ReportsSearchIndexForm(request.POST or None)
    if request.method == "POST" and search_form.is_valid():
        display_search = True
    else:
        display_search = False
    try:
        project = Projects.objects.get(pk=project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    table = ReportsTable({})
    table.set_auth_permissions(auth_permissions)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_REPORTS,
            "title": Reports.TITLE,
            "report_name": Reports.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "table": table,
            "search_form": search_form,
            "display_search": display_search,
            "project":project,
            "index_url": reverse("reports_index",args=[project.project_id]),
            "select_multiple_url": reverse("reports_select_multiple"),
        },
    )


@csrf_exempt
def select_single(request):
    user = Users.login_required(request)
    
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    # if settings.ACCESS_PERMISSION_REPORTS_UPDATE not in auth_permissions.values():
    #     return HttpResponseForbidden("Forbidden", content_type="text/plain")
    action = request.POST["action"]
    id = request.POST["id"]
    comments = request.POST.get("comments")
   

    if action == "" or id is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    try:
        model = Reports.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, Reports.DoesNotExist):
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    
    try:
        project = Projects.objects.get(project_id= model.project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    if action == "submit":
        if (
            model.report_status == Reports.STATUS_DRAFT
            or model.report_status == Reports.STATUS_REJECTED
        ):  
            Methods_Reports.update_status(request, user, model,Reports.STATUS_SUBMITTED,None)
            project_model = Projects.objects.get(pk = model.project_id)
            if project_model.project_status == project_model.STATUS_ASSIGNED:
                Methods_Projects.update_status(request,None,project_model, project_model.STATUS_ACTIVE)
            messages.success(request, "Submitted successfully.")

    
    if action == "accept":
        if settings.ACCESS_PERMISSION_REPORTS_ACCEPT not in auth_permissions.values():
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if (model.report_status == model.STATUS_SUBMITTED or model.report_status == model.STATUS_DENIED):
            Methods_Reports.update_status(
                request, user, model, Reports.STATUS_ACCEPTED, project.project_assigned_to, comments
            )
            messages.success(request, "Accepted successfully.")

    if action == "reject":
        if settings.ACCESS_PERMISSION_REPORTS_REJECT not in auth_permissions.values():
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if (model.report_status == model.STATUS_SUBMITTED or model.report_status == model.STATUS_DENIED):
            Methods_Reports.update_status(
                request, user, model, Reports.STATUS_REJECTED,project.project_assigned_to, comments
            )
            messages.success(request, "Rejected successfully.")

    if action == "approve":
        if settings.ACCESS_PERMISSION_ACTIVITIES_APPROVE not in auth_permissions.values():
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if model.report_status == model.STATUS_ACCEPTED:
            Methods_Reports.update_status(
                request, user, model, model.STATUS_APPROVED, project.project_created_by, comments)
            messages.success(request, "Approved successfully.")

    if action == "deny":
        if settings.ACCESS_PERMISSION_ACTIVITIES_DENY not in auth_permissions.values():
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        if model.report_status == model.STATUS_ACCEPTED:
            Methods_Reports.update_status(
                request, user, model, model.STATUS_DENIED,project.project_created_by,comments)
            messages.success(request, "Denied successfully.")


    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_REPORTS_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        Methods_Reports.delete(request, user, model)
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")


@csrf_exempt
def select_multiple(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_REPORTS_UPDATE not in auth_permissions.values():
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
                model = Reports.objects.get(pk=id)
                if model.report_status == Reports.STATUS_ACTIVE:
                    Methods_Reports.update_status(
                        request, user, model, Reports.STATUS_BLOCKED
                    )
            except (TypeError, ValueError, OverflowError, Reports.DoesNotExist):
                continue
        messages.success(request, "Blocked successfully.")

    if action == "unblock":
        for id in ids:
            try:
                model = Reports.objects.get(pk=id)
                if model.report_status == Reports.STATUS_BLOCKED:
                    Methods_Reports.update_status(
                        request, user, model, Reports.STATUS_INACTIVE
                    )
            except (TypeError, ValueError, OverflowError, Reports.DoesNotExist):
                continue
        messages.success(request, "Unblocked successfully.")

    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_REPORTS_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        for id in ids:
            try:
                model = Reports.objects.get(pk=id)
                Methods_Reports.delete(request, user, model)
            except (TypeError, ValueError, OverflowError, Reports.DoesNotExist):
                continue
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")


def create(request,project_id):
    template_url = "reports/create.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_REPORTS_CREATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    
    try:
        project = Projects.objects.get(pk=project_id)   
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    if request.method == "POST":
        form = ReportsCreateForm(request.POST, user=user)
        funds_transfer_data = request.POST.get("funds_transfer")
        if form.is_valid():
            data = {
                "project_id": project.project_id,
                "asset_name": form.cleaned_data["asset_name"],
                "capital_class": form.cleaned_data["capital_class"],
                "capital_sub_class": form.cleaned_data["capital_sub_class"],
                "purchase_value": form.cleaned_data["purchase_value"],
                "purchase_currency": form.cleaned_data["purchase_currency"],
                "book_value": form.cleaned_data["book_value"],
                "book_currency": form.cleaned_data["book_currency"],
                "year_purchased": form.cleaned_data["year_purchased"],
                "funding_source": form.cleaned_data["funding_source"],
                "fiscal_year": form.cleaned_data["fiscal_year"],
            }
            if len(funds_transfer_data) <= 2:
                err = True
                msg ="Funds transfer is a required field"
            else:
           
                data.update({"funds_transfer_class": funds_transfer_data})
                err, msg, model = Methods_Reports.create(request, user,data)
            if err:
                return JsonResponse({'message':"error", "error":msg})

            return JsonResponse({'report_id': model.report_id, 'message':"success", "msg":msg})
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_REPORTS,
                    "title": Reports.TITLE,
                    "name": Reports.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "project" : project
                    
                },
            )

    form = ReportsCreateForm(user=user)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_REPORTS,
            "title": Reports.TITLE,
            "name": Reports.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "project" : project
        },
    )


def update(request, pk):
    template_url = "reports/update.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_REPORTS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Reports.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Reports.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        project = Projects.objects.get(pk=model.project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    if request.method == "POST":
        form = ReportsUpdateForm(request.POST, user=user)
        funds_transfer_data = request.POST.get("funds_transfer")
        if form.is_valid():
            data = {
                "asset_name": form.cleaned_data["asset_name"],
                "capital_class": form.cleaned_data["capital_class"],
                "capital_sub_class": form.cleaned_data["capital_sub_class"],
                "purchase_value": form.cleaned_data["purchase_value"],
                "purchase_currency": form.cleaned_data["purchase_currency"],
                "book_value": form.cleaned_data["book_value"],
                "book_currency": form.cleaned_data["book_currency"],
                "year_purchased": form.cleaned_data["year_purchased"],
                "funding_source": form.cleaned_data["funding_source"],
                "fiscal_year": form.cleaned_data["fiscal_year"],   
            }
            if funds_transfer_data is not None:
                data.update({"funds_transfer_class": funds_transfer_data})
                err, msg, model = Methods_Reports.update(request, user,data, model)
                if err:
                    messages.error(request, msg)
                    return render(
                        request,
                        template_url,
                        {
                            "section": settings.BACKEND_SECTION_REPORTS,
                            "title": Reports.TITLE,
                            "name": Reports.NAME,
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
                        settings.MODEL_REPORTS,
                        model.report_id,
                        "Updated reports.",
                        user.user_id,
                        user.user_name,
                    )
                )
                return JsonResponse({'report_id': model.report_id, 'message':"success"})
                #return redirect(reverse("reports_view", args=[model.report_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_REPORTS,
                    "title": Reports.TITLE,
                    "name": Reports.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "model": model,
                    "project": project,
                },
            )

    form = ReportsUpdateForm(
        user=user, initial=Methods_Reports.form_view(request, user, model)
    )
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_REPORTS,
            "title": Reports.TITLE,
            "name": Reports.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "model": model,
            "project":project
        },
    )


def view(request, pk):
    
    template_url = "reports/view.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    try:
        model = Reports.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Reports.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        project = Projects.objects.get(pk=model.project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    model = Methods_Reports.format_view(request, user, model)
    form = ReportsViewForm(
        user=user, initial=Methods_Reports.form_view(request, user, model)
    )
    count_logs = Methods_Mongo.get_collection(settings.MODEL_LOGS).count_documents(
        {"model": "reports", "modelId": model.report_id}
    )
    form_comments = CommentsCreateForm(user=None)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_PROJECTS,
            "title": Reports.TITLE,
            "name": Reports.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "model": model,
            "form": form,
            "project":project,
             "form_comments":form_comments,
            "index_url": reverse("projects_view",args=[project.project_id]),
            "select_single_url": reverse("reports_select_single"),
            "count_logs": count_logs,
        },
    )
