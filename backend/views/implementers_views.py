import asyncio
import json
from django.contrib import messages

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseForbidden,
    JsonResponse,
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.urls import reverse

from app import settings
from app.utils import Utils
from app.models.implementers import Implementers
from app.models.methods.implementers import Methods_Implementers
from app.models.methods.logs import Methods_Logs
from app.models.methods.files import Methods_Files
from app.models.methods.users import Methods_Users
from app.models.users import Users
from app.models.organizations import Organizations
from backend.tables.implementers_tables_view import ImplementersTableView


class AjaxImplementersListView(View):
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
        Methods_Users.get_auth_permissions(user)
        # user_notifications = Methods_Users.get_notifications(user)
        # office_user, office_user_uid, office_user_params = Methods_Users.get_office_params(user)

        datatables = request.GET

        model = datatables.get("model")
        modelId = int(datatables.get("model_id"))
        section = datatables.get("section")
        userId = datatables.get("user_id")

        # item draw
        draw = int(datatables.get("draw"))
        # item start
        start = int(datatables.get("start"))
        # item length (limit)
        length = int(datatables.get("length"))
        # item data search
        # search = datatables.get('search[value]')

        # Get objects
        objects = Implementers.objects
        objects = objects.filter(Q(implementer_model=model) & Q(implementer_model_id=modelId))

        # Set record total
        records_total = objects.all().count()
        # Set records filtered
        records_filtered = records_total

        objects = objects.order_by("-implementer_id")

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
            value1 = ImplementersTableView.render_implementer_name(record)
            value4 = ImplementersTableView.render_implementer_updated_at(record)
            value5 = ImplementersTableView.render_implementer_updated_by(record)

            data.append(
                {
                    "implementer_name": value1,
                    "implementer_updated_at": value4,
                    "implementer_updated_by": value5,
                }
            )

        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }


@csrf_exempt
def create(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")

    name = request.POST["name"]

    if name == "":
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    data = {
        "name": name,
    }
    err, msg, model = Methods_Implementers.create(request, user, data)
    if err:
        messages.error(request, msg)
    else:
        messages.success(request, "Created successfully.")
    return redirect(reverse("projects_create",))

@csrf_exempt
def get_all_implementers (request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    values = ""
    try:
        organizations = Organizations.objects.all()
    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    try:
        implementers = Implementers.objects.all()
    except (TypeError, ValueError, OverflowError, Implementers.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    for organization in organizations:
            values += (
            "<option value='"
            +str(organization.organization_id)
            + "'>"
            + str(organization.organization_name)
            + "</option>"
        )
                
    for implementer in implementers:
            values += (
            "<option value='"
            +"impl_"+str(implementer.implementer_id)
            + "'>"
            + str(implementer.implementer_name)
            + "</option>"
        )
    return HttpResponse(values, content_type="text/plain")

