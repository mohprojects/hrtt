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
from app.models.currency_rates import Currency_Rates
from app.models.projects import Projects
from app.models.methods.currency_rates import Methods_Currency_Rates
from app.models.methods.logs import Methods_Logs
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.users import Methods_Users
from app.models.users import Users
from backend.tables.currency_rates import CurrencyRatesTable
from backend.forms.currency_rates import (CurrencyRatesCreateForm, 
                                          CurrencyRatesSearchIndexForm,
                                          CurrencyRatesUpdateForm,
                                          CurrencyRatesViewForm)


class AjaxCurrencyRatesListView(View):
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
        column1 = "rate_fiscal_year"
        column2 = "rate_currency"
        column3 = "rate_rate"
        
        datatables = request.GET

        # item draw
        draw = int(datatables.get("draw"))
        # item start
        start = int(datatables.get("start"))
        # item length (limit)
        length = int(datatables.get("length"))

        # Get objects
        #objects = CurrencyRates.objects.all()
        objects = Currency_Rates.objects.filter()
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
            row_number = CurrencyRatesTable.render_row_number(record, counter)
            value2 = CurrencyRatesTable.render_rate_fiscal_year(record)
            value3 = CurrencyRatesTable.render_rate_currency(record)
            value6 = CurrencyRatesTable.render_rate_rate(record)
            actions = CurrencyRatesTable.render_actions(record, auth_permissions)

            data.append(
                {
                    "row_number": row_number,
                    "rate_fiscal_year": value2,
                    "rate_currency": value3,
                    "rate_rate": value6,
                    "actions": actions,
                }
            )

        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }
    


def json_currency_rates(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_CURRENCY_RATES_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    return HttpResponse(
        serializers.serialize("json", Currency_Rates.objects.all()),
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
        model = Currency_Rates.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, Currency_Rates.DoesNotExist):
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    if action == "delete":
        if (settings.ACCESS_PERMISSION_CURRENCY_RATES_DELETE not in auth_permissions.values()):
            return HttpResponseForbidden("Forbidden", content_type="text/plain")
        Methods_Currency_Rates.delete(request, user, model)
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
                model = Currency_Rates.objects.get(pk=id)
                Methods_Currency_Rates.delete(request, user, model)
            except (TypeError, ValueError, OverflowError, Currency_Rates.DoesNotExist):
                continue
        messages.success(request, "Deleted successfully.")

    return HttpResponse("success", content_type="text/plain")

def index(request):
    template_url = "currency_rates/index.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_LEVELS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    search_form = CurrencyRatesSearchIndexForm(request.POST or None)
    if request.method == "POST" and search_form.is_valid():
        display_search = True
    else:
        display_search = False

    table = CurrencyRatesTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_LEVELS,
            "title": Currency_Rates.TITLE,
            "name": Currency_Rates.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "table": table,
            "search_form": search_form,
            "display_search": display_search,
            "index_url": reverse("currency_rates_index"),
            "select_multiple_url": reverse("currency_rates_select_multiple"),
        },
    )


def create(request):
    template_url = "currency_rates/create.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_CURRENCY_RATES_CREATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    if request.method == "POST":
        form = CurrencyRatesCreateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "fiscal_year":form.cleaned_data["fiscal_year"],
                "currency":form.cleaned_data["currency"],
                "rate" : form.cleaned_data["rate"],
            }
            err, msg, model = Methods_Currency_Rates.create(request, user, data)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                        "title": Currency_Rates.TITLE,
                        "name": Currency_Rates.NAME,
                        "user": user,
                        "auth_permissions": auth_permissions,
                        "form": form,
                    },
                )
            messages.success(request, "Created successfully.")
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_RATES,
                    model.rate_id,
                    "Created Currency Rate.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("currency_rates_view", args=[model.rate_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                    "title": Currency_Rates.TITLE,
                    "name": Currency_Rates.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    
                },
            )

    form = CurrencyRatesCreateForm(user=user)
    return render(
        request,
        template_url,
        {
            "section":settings.BACKEND_SECTION_CURRENCY_RATES,
            "title": Currency_Rates.TITLE,
            "name": Currency_Rates.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
        },
    )

def update(request, pk):
    template_url = "currency_rates/update.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_CURRENCY_RATES_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Currency_Rates.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Currency_Rates.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    if request.method == "POST":
        form = CurrencyRatesUpdateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "fiscal_year":form.cleaned_data["fiscal_year"],
                "rate" : form.cleaned_data["rate"],
                "currency":form.cleaned_data["currency"]
            }
            err, msg, model = Methods_Currency_Rates.update(request, user, data, model)
            if err:
                messages.error(request, msg)
                return render(
                    request,
                    template_url,
                    {
                        "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                        "title": Currency_Rates.TITLE,
                        "name": Currency_Rates.NAME,
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
                    model.rate_id,
                    "Updated currency rates.",
                    user.user_id,
                    user.user_name,
                )
            )
            return redirect(reverse("currency_rates_view", args=[model.rate_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request,
                template_url,
                {
                    "section": settings.BACKEND_SECTION_CURRENCY_RATES,
                    "title": Currency_Rates.TITLE,
                    "name": Currency_Rates.NAME,
                    "user": user,
                    "auth_permissions": auth_permissions,
                    "form": form,
                    "model": model,
                },
            )

    form = CurrencyRatesUpdateForm(
        user=user, initial=Methods_Currency_Rates.form_view(request, user, model)
    )
    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_CURRENCY_RATES,
            "title": Currency_Rates.TITLE,
            "name": Currency_Rates.NAME,
            "user": user,
            "auth_permissions": auth_permissions,
            "form": form,
            "model": model,
        },
    )



def view(request, pk):
    template_url = "currency_rates/view.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_CURRENCY_RATES_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    try:
        model = Currency_Rates.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Currency_Rates.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    
    model = Methods_Currency_Rates.format_view(request, user, model)
    form =CurrencyRatesViewForm(
        user=user, initial=Methods_Currency_Rates.form_view(request, user, model)
    )
    
    count_logs = Methods_Mongo.get_collection(settings.MODEL_LOGS).count_documents(
        {"model": "CurrencyRates", "modelId": model.rate_id}
    )

    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_CURRENCY_RATES,
            "title": "CurrencyRates",
            "name": "CurrencyRates",
            "user": user,
            "auth_permissions": auth_permissions,
            "model": model,
            "form": form,
            "index_url": reverse("currency_rates_index"),
            "select_single_url": reverse("currency_rates_select_single"),
            "count_logs": count_logs,
        },
    )







