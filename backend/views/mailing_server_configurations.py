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
)
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app import settings
from app.models.mailing_server_configurations import MailServerConfig
from app.models.methods.mailing_server_configurations import Methods_MailServerConfig
from app.models.methods.logs import Methods_Logs
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.users import Methods_Users
from app.models.users import Users
from backend.forms.mailing_server_configurations_forms import (MailServerConfigCreateForm, 
                                          MailServerConfigSearchIndexForm,
                                          MailServerConfigUpdateForm,
                                          MailServerConfigViewForm)


# class AjaxMailServerConfigListView(View):
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
#         column1 = "fiscal_year"
#         column2 = "host"
#         column3 = "port"
#         column4 = "username"
#         column5 = "password"
        
#         datatables = request.GET

#         # item draw
#         draw = int(datatables.get("draw"))
#         # item start
#         start = int(datatables.get("start"))
#         # item length (limit)
#         length = int(datatables.get("length"))

#         # Get objects
#         #objects = MailServerConfig.objects.all()
#         objects = MailServerConfig.objects.filter()
#         # Set record total
#         records_total = objects.all().count()
#         # Set records filtered
#         records_filtered = records_total
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

#         objects_filter = False

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
#             row_number = MailServerConfigTable.render_row_number(record, counter)
#             value1 = MailServerConfigTable.render_fiscal_year(record)
#             value2 = MailServerConfigTable.render_host(record)
#             value3 = MailServerConfigTable.render_port(record)
#             value4 = MailServerConfigTable.render_username(record)
#             value5 = MailServerConfigTable.render_password(record)
#             actions = MailServerConfigTable.render_actions(record, auth_permissions)

#             data.append(
#                 {
#                     "row_number": row_number,
#                     "fiscal_year": value1,
#                     "host": value2,
#                     "port": value3,
#                     "username": value4,
#                     "password": value5,
#                     "actions": actions,
#                 }
#             )

#         return {
#             "draw": draw,
#             "recordsTotal": records_total,
#             "recordsFiltered": records_filtered,
#             "data": data,
#         }
    


# def json_mailing_server_configurations(request):
#     user = Users.login_required(request)
#     if user is None:
#         Users.set_redirect_field_name(request, request.path)
#         return redirect(reverse("users_signin"))
#     auth_permissions = Methods_Users.get_auth_permissions(user)
#     if settings.ACCESS_PERMISSION_CURRENCY_RATES_VIEW not in auth_permissions.values():
#         return HttpResponseForbidden("Forbidden", content_type="text/plain")
#     return HttpResponse(
#         serializers.serialize("json", MailServerConfig.objects.all()),
#         content_type="application/json",
#     )
    
    
@csrf_exempt
def select_single(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
   
    action = request.POST["action"]
    id = request.POST["id"]

    if action == "" or id is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    try:
        model = MailServerConfig.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, MailServerConfig.DoesNotExist):
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    if action == "delete":
        if (settings.ACCESS_PERMISSION_CURRENCY_RATES_DELETE not in auth_permissions.values()):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        Methods_MailServerConfig.delete(request, user, model)
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")

@csrf_exempt
def select_multiple(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
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
            settings.ACCESS_PERMISSION_CURRENCY_RATES_DELETE
            not in auth_permissions.values()
        ):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        for id in ids:
            try:
                model = MailServerConfig.objects.get(pk=id)
                Methods_MailServerConfig.delete(request, user, model)
            except (TypeError, ValueError, OverflowError, MailServerConfig.DoesNotExist):
                continue
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")

# def index(request):
#     template_url = "mailing_server_configurations/index.html"
#     user = Users.login_required(request)
#     if user is None:
#         Users.set_redirect_field_name(request, request.path)
#         return redirect(reverse("users_signin"))
#     auth_permissions = Methods_Users.get_auth_permissions(user)
#     if settings.ACCESS_PERMISSION_LEVELS_VIEW not in auth_permissions.values():
#         return HttpResponseForbidden("Forbidden", content_type="text/plain")

#     search_form = MailServerConfigSearchIndexForm(request.POST or None)
#     if request.method == "POST" and search_form.is_valid():
#         display_search = True
#     else:
#         display_search = False

#     table = MailServerConfigTable({})
#     # table.paginate(page=request.GET.get('page', 1), per_page=5)
#     table.set_auth_permissions(auth_permissions)
#     return render(
#         request,
#         template_url,
#         {
#             "section": settings.BACKEND_SECTION_CONFIGURABLES,
#             "title": MailServerConfig.TITLE,
#             "name": MailServerConfig.NAME,
#             "user": user,
#             "auth_permissions": auth_permissions,
#             "table": table,
#             "search_form": search_form,
#             "display_search": display_search,
#             "index_url": reverse("mailing_server_configurations_index"),
#             "select_multiple_url": reverse("mailing_server_configurations_select_multiple"),
#         },
#     )


def create(request):
    template_url = "email/configure.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    # if settings.ACCESS_PERMISSION_CURRENCY_RATES_CREATE not in auth_permissions.values():
    #     return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        config = MailServerConfig.objects.first()
    except (TypeError, ValueError, OverflowError, MailServerConfig.DoesNotExist):
        # return HttpResponseNotFound("Not Found", content_type="text/plain")
        pass

    if request.method == "POST":
        form = MailServerConfigCreateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "host":form.cleaned_data["host"],
                "port" : form.cleaned_data["port"],
                "username":form.cleaned_data["username"],
                "password" : form.cleaned_data["password"],
                "sender":form.cleaned_data["sender"],
                "subject" : form.cleaned_data["subject"],
                "tls":form.cleaned_data["tls"],
                "ssl" : form.cleaned_data["ssl"],

            }
            if config is not None:
                err, msg, model = Methods_MailServerConfig.update(request, user, data, config)
            else:
                err, msg, model = Methods_MailServerConfig.create(request, user, data)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                        # "title": MailServerConfig.TITLE,
                        # "name": MailServerConfig.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                    },
                )
            messages.success(request, "Created successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_RATES,
                    model.id,
                    "Created Currency Rate.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("mail_configuration_view", args=[model.id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                    # "title": MailServerConfig.TITLE,
                    # "name": MailServerConfig.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    
                },
            )
    if config is not None:
        form = MailServerConfigUpdateForm(
        user=user, initial=Methods_MailServerConfig.form_view(request, user, config)
    )
    else:
        form = MailServerConfigCreateForm(user=user)
    return render(
        request,
        template_url,
        {
            "section":settings.BACKEND_SECTION_CURRENCY_RATES,
            # "title": MailServerConfig.TITLE,
            # "name": MailServerConfig.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
        },
    )

def update(request, pk):
    template_url = "mailing_server_configurations/update.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_CURRENCY_RATES_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = MailServerConfig.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, MailServerConfig.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    if request.method == "POST":
        form = MailServerConfigUpdateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "host":form.cleaned_data["host"],
                "port" : form.cleaned_data["port"],
                "username":form.cleaned_data["username"],
                "password" : form.cleaned_data["password"],
            }
            err, msg, model = Methods_MailServerConfig.update(request, user, data, model)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                        # "title": MailServerConfig.TITLE,
                        # "name": MailServerConfig.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                        "model": model,
                    },
                )
            messages.success(request, "Updated successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_RATES,
                    model.id,
                    "Updated host rates.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("mailing_server_configurations_view", args=[model.id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                    # "title": MailServerConfig.TITLE,
                    # "name": MailServerConfig.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "model": model,
                },
            )

    form = MailServerConfigUpdateForm(
        user=user, initial=Methods_MailServerConfig.form_view(request, user, model)
    )
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_CURRENCY_RATES,
            # "title": MailServerConfig.TITLE,
            # "name": MailServerConfig.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "model": model,
        },
    )


def view(request, pk):
    template_url = "email/configuration_view.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_CURRENCY_RATES_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = MailServerConfig.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, MailServerConfig.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    model = Methods_MailServerConfig.format_view(request, user, model)
    form =MailServerConfigViewForm(
        user=user, initial=Methods_MailServerConfig.form_view(request, user, model)
    )
    
    # count_logs = Methods_Mongo.get_collection(settings.MODEL_LOGS).count_documents(
    #     {"model": "MailServerConfig", "modelId": model.id}
    # )

    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_CURRENCY_RATES,
            # "title": MailServerConfig.TITLE,
            # "name": MailServerConfig.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "model": model,
            "form": form,
           # "select_single_url": reverse("mailing_server_configurations_select_single"),
        },
    )