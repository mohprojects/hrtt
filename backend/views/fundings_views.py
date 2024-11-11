import asyncio
import json
from django.contrib import messages

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
    JsonResponse
)
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app import settings
from app.utils import Utils
from app.models.fundings import Fundings
from app.models.projects import Projects
from app.models.methods.fundings import Methods_Fundings
from app.models.methods.projects import Methods_Projects
from app.models.methods.logs import Methods_Logs
from app.models.methods.mongo import Methods_Mongo
#from app.models.methods.files import Methods_Files
from app.models.methods.users import Methods_Users
from app.models.users import Users
from backend.tables.fundings_tables_view import FundingsTableView
from backend.forms.fundings_forms import (FundingsCreateForm, 
                                          FundingsSearchIndexForm,
                                          FundingsUpdateForm,
                                          FundingsViewForm)


class AjaxFundingsListView(View):
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
        column1 = "funder_id"
        column2 = "funding_amount"
        column3 = "funding_currency"
        column4 = "funding_updated_at"
        column5 = "funding_status"
        
        datatables = request.GET
        project_id = datatables.get("project_id")
        project_organization = datatables.get("project_organization")

        # item draw
        draw = int(datatables.get("draw"))
        # item start
        start = int(datatables.get("start"))
        # item length (limit)
        length = int(datatables.get("length"))
        # item data search
        # search = datatables.get('search[value]')

        # Get objects
        #objects = Fundings.objects.all()
        objects = Fundings.objects.filter(Q(project_id=project_id) )
        # Set record total
        records_total = objects.all().count()
        # Set records filtered
        records_filtered = records_total
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


        objects_filter = False

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
            row_number = FundingsTableView.render_row_number(record, counter)
            value2 = FundingsTableView.render_funder_id(record)
            value3 = FundingsTableView.render_funding_amount(record)
            value4 = FundingsTableView.render_funding_updated_at(record)
            value6 = FundingsTableView.render_funding_currency(record)
            actions = FundingsTableView.render_actions(record, auth_permissions, user, project_organization)

            data.append(
                {
                    "row_number": row_number,
                    "funder_id": value2,
                    "funding_amount": value3,
                    "funding_currency": value6,
                    "funding_updated_at": value4,
                    "actions": actions,
                }
            )

        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }
    
    
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
        model = Fundings.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, Fundings.DoesNotExist):
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")


    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_PROJECTS_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        Methods_Fundings.delete(request, user, model)
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


    if action == "delete":
        if (
            settings.ACCESS_PERMISSION_PROJECTS_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        for id in ids:
            try:
                model = Fundings.objects.get(pk=id)
                Methods_Fundings.delete(request, user, model)
            except (TypeError, ValueError, OverflowError, Fundings.DoesNotExist):
                continue
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")



def create(request,project_id):
    template_url = "fundings/create.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_PROJECTS_CREATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        project = Projects.objects.get(pk=project_id)
        
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")

    if request.method == "POST":
        form = FundingsCreateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "project": project.project_id,
                "organization":form.cleaned_data["organization"],
                "amount" : form.cleaned_data["amount"],
                "currency":form.cleaned_data["currency"]
            }
            err, msg, model = Methods_Fundings.create(request, user, data)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_PROJECTS,
                        "title": Fundings.TITLE,
                        "name": Fundings.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                        "project":project
                    },
                )
            Methods_Projects.update_tags(request,project)
            messages.success(request, "Created successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_FUNDINGS,
                    model.funding_id,
                    "Created Fundings.",
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
                    "title": Fundings.TITLE,
                    "name": Fundings.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    
                },
            )

    form = FundingsCreateForm(user=user)
    return render(
        request,
        template_url,
        {
            "section":settings.BACKEND_SECTION_PROJECTS,
            "title": Fundings.TITLE,
            "name": Fundings.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "project":project
        },
    )

def update(request, pk):
    template_url = "fundings/update.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_PROJECTS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Fundings.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Fundings.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        project = Projects.objects.get(pk=model.project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    if request.method == "POST":
        form = FundingsUpdateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "project": project.project_id,
                "organization":form.cleaned_data["organization"],
                "amount" : form.cleaned_data["amount"],
                "currency":form.cleaned_data["currency"]
            }
            err, msg, model = Methods_Fundings.update(request, user, data, model)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_PROJECTS,
                        "title": Fundings.TITLE,
                        "name": Fundings.NAME,
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
                    settings.MODEL_PROJECTS,
                    model.funding_id,
                    "Updated fundings.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("fundings_view", args=[model.funding_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_PROJECTS,
                    "title": Fundings.TITLE,
                    "name": Fundings.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "model": model,
                    "project": project,
                },
            )

    form = FundingsUpdateForm(
        user=user, initial=Methods_Fundings.form_view(request, user, model)
    )
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_PROJECTS,
            "title": Fundings.TITLE,
            "name": Fundings.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "model": model,
            "project":project
        },
    )



def view(request, pk):
    template_url = "fundings/view.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_PROJECTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Fundings.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Fundings.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        project = Projects.objects.get(project_id=model.project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    model = Methods_Fundings.format_view(request, user, model)
    form =FundingsViewForm(
        user=user, initial=Methods_Fundings.form_view(request, user, model)
    )
    
    count_logs = Methods_Mongo.get_collection(settings.MODEL_LOGS).count_documents(
        {"model": "Fundings", "modelId": model.funding_id}
    )

    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_PROJECTS,
            "title": "Fundings",
            "name": "Fundings",
            "user": user,
            "auth_permissions": auth_permissions,
            "model": model,
            "form": form,
            "project":project,
            "index_url": reverse("projects_view",args=[project.project_id]),
            "select_single_url": reverse("fundings_select_single"),
            "count_logs": count_logs,
        },
    )







