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
from app.models.gdp_populations import Gdp_Populations
from app.models.methods.gdp_populations import Methods_Gdp_Populations
from app.models.methods.logs import Methods_Logs
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.users import Methods_Users
from app.models.users import Users
from backend.tables.gdp_populations import GdpPopulationsTable
from backend.forms.gdp_populations_forms import (GdpPopulationsCreateForm, 
                                          GdpPopulationsSearchIndexForm,
                                          GdpPopulationsUpdateForm,
                                          GdpPopulationsViewForm)


class AjaxGdpPopulationsListView(View):
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
        column1 = "fiscal_year"
        column2 = "population"
        column3 = "budget"
        column4 = "expenditure"
        column5 = "gdp"
        column6 = "payment_rate"
        column7 = "budget_health"
        column8 =  "expenditure_health"
        
        
        datatables = request.GET

        # item draw
        draw = int(datatables.get("draw"))
        # item start
        start = int(datatables.get("start"))
        # item length (limit)
        length = int(datatables.get("length"))

        # Get objects
        #objects = GdpPopulations.objects.all()
        objects = Gdp_Populations.objects.filter()
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
            row_number = GdpPopulationsTable.render_row_number(record, counter)
            value1 = GdpPopulationsTable.render_fiscal_year(record)
            value2 = GdpPopulationsTable.render_population(record)
            value3 = GdpPopulationsTable.render_budget(record)
            value4 = GdpPopulationsTable.render_expenditure(record)
            value5 = GdpPopulationsTable.render_gdp(record)
            value6 = GdpPopulationsTable.render_payment_rate(record)
            value7 = GdpPopulationsTable.render_budget_health(record)
            value8 =  GdpPopulationsTable.render_expenditure_health(record)
            actions = GdpPopulationsTable.render_actions(record, auth_permissions)

            data.append(
                {
                    "row_number": row_number,
                    "fiscal_year": value1,
                    "population": value2,
                    "budget": value3,
                    "expenditure": value4,
                    "gdp": value5,
                    "payment_rate": value6,
                    "budget_health" : value7,
                    "expenditure_health" : value8,
                    "actions": actions,
                }
            )

        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }
    


def json_gdp_populations(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_CURRENCY_RATES_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    return HttpResponse(
        serializers.serialize("json", Gdp_Populations.objects.all()),
        content_type="application/json",
    )
    
    
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
        model = Gdp_Populations.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, Gdp_Populations.DoesNotExist):
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    if action == "delete":
        if (settings.ACCESS_PERMISSION_CURRENCY_RATES_DELETE not in auth_permissions.values()):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        Methods_Gdp_Populations.delete(request, user, model)
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
                model = Gdp_Populations.objects.get(pk=id)
                Methods_Gdp_Populations.delete(request, user, model)
            except (TypeError, ValueError, OverflowError, Gdp_Populations.DoesNotExist):
                continue
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")

def index(request):
    template_url = "gdp_populations/index.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_LEVELS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    search_form = GdpPopulationsSearchIndexForm(request.POST or None)
    if request.method == "POST" and search_form.is_valid():
        display_search = True
    else:
        display_search = False

    table = GdpPopulationsTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_CONFIGURABLES,
            "title": Gdp_Populations.TITLE,
            "name": Gdp_Populations.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "table": table,
            "search_form": search_form,
            "display_search": display_search,
            "index_url": reverse("gdp_populations_index"),
            "select_multiple_url": reverse("gdp_populations_select_multiple"),
        },
    )


def create(request):
    template_url = "gdp_populations/create.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_CURRENCY_RATES_CREATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    if request.method == "POST":
        form = GdpPopulationsCreateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "fiscal_year":form.cleaned_data["fiscal_year"],
                "population":form.cleaned_data["population"],
                "budget":form.cleaned_data["budget"],
                "expenditure" : form.cleaned_data["expenditure"],
                "gdp" : form.cleaned_data["gdp"],
                "payment_rate" : form.cleaned_data["payment_rate"],
                "budget_health":form.cleaned_data["budget_health"],
                "expenditure_health" : form.cleaned_data["expenditure_health"],
            }
            err, msg, model = Methods_Gdp_Populations.create(request, user, data)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                        "title": Gdp_Populations.TITLE,
                        "name": Gdp_Populations.NAME,
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
            return redirect(reverse("gdp_populations_view", args=[model.id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                    "title": Gdp_Populations.TITLE,
                    "name": Gdp_Populations.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    
                },
            )

    form = GdpPopulationsCreateForm(user=user)
    return render(
        request,
        template_url,
        {
            "section":settings.BACKEND_SECTION_CURRENCY_RATES,
            "title": Gdp_Populations.TITLE,
            "name": Gdp_Populations.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
        },
    )

def update(request, pk):
    template_url = "gdp_populations/update.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_CURRENCY_RATES_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Gdp_Populations.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Gdp_Populations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    if request.method == "POST":
        form = GdpPopulationsUpdateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "fiscal_year":form.cleaned_data["fiscal_year"],
                "population":form.cleaned_data["population"],
                "budget":form.cleaned_data["budget"],
                "expenditure" : form.cleaned_data["expenditure"],
                "gdp" : form.cleaned_data["gdp"],
                "payment_rate" : form.cleaned_data["payment_rate"],
                "budget_health":form.cleaned_data["budget_health"],
                "expenditure_health" : form.cleaned_data["expenditure_health"],
            }
            err, msg, model = Methods_Gdp_Populations.update(request, user, data, model)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                        "title": Gdp_Populations.TITLE,
                        "name": Gdp_Populations.NAME,
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
                    "Updated population rates.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("gdp_populations_view", args=[model.id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                    "title": Gdp_Populations.TITLE,
                    "name": Gdp_Populations.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "model": model,
                },
            )

    form = GdpPopulationsUpdateForm(
        user=user, initial=Methods_Gdp_Populations.form_view(request, user, model)
    )
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_CURRENCY_RATES,
            "title": Gdp_Populations.TITLE,
            "name": Gdp_Populations.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "model": model,
        },
    )


def view(request, pk):
    template_url = "gdp_populations/view.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_CURRENCY_RATES_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Gdp_Populations.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Gdp_Populations.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    model = Methods_Gdp_Populations.format_view(request, user, model)
    form =GdpPopulationsViewForm(
        user=user, initial=Methods_Gdp_Populations.form_view(request, user, model)
    )
    
    count_logs = Methods_Mongo.get_collection(settings.MODEL_LOGS).count_documents(
        {"model": "GdpPopulations", "modelId": model.id}
    )

    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_CURRENCY_RATES,
            "title": Gdp_Populations.TITLE,
            "name": Gdp_Populations.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "model": model,
            "form": form,
            "index_url": reverse("gdp_populations_index"),
            "select_single_url": reverse("gdp_populations_select_single"),
            "count_logs": count_logs,
        },
    )







