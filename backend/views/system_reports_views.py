
import json
import redis
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app import settings
from app.utils import Utils
from app.models.activities import Activities
from app.models.activities_inputs import Activities_Inputs
from app.models.currency_rates import Currency_Rates
from app.models.gdp_populations import Gdp_Populations
from app.models.methods.gdp_populations import Methods_Gdp_Populations
from app.models.levels import Levels
from app.models.methods.users import Methods_Users
from app.models.organizations import Organizations
from app.models.projects import Projects
from app.models.users import Users

redis_client = redis.StrictRedis.from_url(settings.CELERY_BROKER_URL)

def index(request, pk):
    template_url = None
    if pk == '1':
        template_url = "system-reports/table-1-budget.html"
    if pk == '2':
        template_url = "system-reports/table-1-expenditure.html"
    if pk == '3':
        template_url = "system-reports/table-2-budget.html"
    if pk == '4':
        template_url = "system-reports/table-2-expenditure.html"
    if pk == '5':
        template_url = "system-reports/table-3-budget.html"
    if pk == '6':
        template_url = "system-reports/table-3-expenditure.html"
    if pk == '7':
        template_url = "system-reports/figure-1-budget.html"
    if pk == '8':
        template_url = "system-reports/figure-1-expenditure.html"
    if pk == '9':
        template_url = "system-reports/figure-2-budget.html"
    if pk == '10':
        template_url = "system-reports/figure-2-expenditure.html"
    if pk == '11':
        template_url = "system-reports/figure-3-budget.html"
    if pk == '12':
        template_url = "system-reports/figure-3-expenditure.html"
    if pk == '13':
        template_url = "system-reports/figure-4-budget.html"
    if pk == '14':
        template_url = "system-reports/figure-4-expenditure.html"
    if pk == '15':
        template_url = "system-reports/figure-5-budget.html"
    if pk == '16':
        template_url = "system-reports/figure-5-expenditure.html"
    if pk == '17':
        template_url = "system-reports/table-4-budget.html"
    if pk == '18':
        template_url = "system-reports/table-4-expenditure.html"
    if pk == '19':
        template_url = "system-reports/table-5-budget.html"
    if pk == '20':
        template_url = "system-reports/table-5-expenditure.html"
    if pk == '21':
        template_url = "system-reports/table-6-budget.html"
    if pk == '22':
        template_url = "system-reports/table-6-expenditure.html"
    if pk == '23':
        template_url = "system-reports/table-7-budget.html"
    if pk == '24':
        template_url = "system-reports/table-7-expenditure.html"
    if pk == '25':
        template_url = "system-reports/table-8-budget.html"
    if pk == '26':
        template_url = "system-reports/table-8-expenditure.html"
    if pk == '27':
        template_url = "system-reports/table-9-budget.html"
    if pk == '28':
        template_url = "system-reports/table-9-expenditure.html"
    if pk == '29':
        template_url = "system-reports/figure-6-budget.html"
    if pk == '30':
        template_url = "system-reports/figure-6-expenditure.html"
    if pk == '31':
        template_url = "system-reports/figure-7-budget.html"
    if pk == '32':
        template_url = "system-reports/figure-7-expenditure.html"
    if pk == '33':
        template_url = "system-reports/figure-8-budget.html"
    if pk == '34':
        template_url = "system-reports/figure-8-expenditure.html"
        

    if template_url is None:
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)

    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    
    # get years
    fiscal_year_choices = Utils.get_fiscal_year_choices_for_system_report()

    return render(
        request,
        template_url,
        {
            "section": settings.BACKEND_SECTION_SYSTEM_REPORTS,
            "title": 'Reports',
            "name": 'Reports',
            "user": user,
            "fiscal_year_choices":fiscal_year_choices,
            "auth_permissions": auth_permissions,
            "index_url": reverse("system_reports_index", kwargs={'pk': pk}),
        },
    )
    


@csrf_exempt
def get_gdp(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    items = Gdp_Populations.objects.filter(fiscal_year=year)
    if len(items) == 0:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    item = items[0]

    data = {
        "year": year,
        "population": item.population,
        "budget": item.budget,
        "expenditure": item.expenditure,
        "gdp": item.gdp,
        "payment_rate": item.payment_rate,
        "budget_health": item.budget_health,
        "expenditure_health": item.expenditure_health,
    }

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_exchange_rate(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    currency = request.POST["currency"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    items = Currency_Rates.objects.filter(
        Q(rate_fiscal_year=year) &
        Q(rate_currency=currency)
    )
    
    if len(items) == 0:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    item = items[0]
   
    data = {
        "year": year,
        "currency": item.rate_currency,
        "rate": item.rate_rate,
    }

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_public_health(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]
   
    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'2', '3','4','5','10','13'}))
    organizations_ids = Organizations.objects.values_list(
        'organization_id', flat=True).filter(
        Q(organization_type__in= set(ids)))

    projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
        Q(organization_id__in=set(organizations_ids))
    )

    if type == 'budget':
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)
            # Q(activity_status=3)  # budger approved
        )
    if type == 'expenditure':
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)
            # Q(activity_status=4)  # expenditure approved
        )

    if type == 'budget':
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(Q(level_code='FS.1'))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
             Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
             Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
    if type == 'expenditure':
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(Q(level_code='FS.1'))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # expenditure approved
        )

    amount = 0
    for item in activities_inputs:
        if type == 'budget':
            if item.activity_input_budget_currency == 'RWF':
                amount += item.activity_input_budget
            else:
                rates = Currency_Rates.objects.filter(
                    Q(rate_fiscal_year=year) &
                    Q(rate_currency=item.activity_input_budget_currency)
                )
                if len(rates) == 0:
                    amount += 0
                else:
                    rate = rates[0]
                    amt = item.activity_input_budget * rate.rate_rate
                    amount += amt

        if type == 'expenditure':
            if item.activity_input_expenses_currency == 'RWF':
                amount += item.activity_input_expenses
            else:
                rates = Currency_Rates.objects.filter(
                    Q(rate_fiscal_year=year) &
                    Q(rate_currency=item.activity_input_expenses_currency)
                )
                if len(rates) == 0:
                    amount += 0
                else:
                    rate = rates[0]
                    amt = item.activity_input_expenses * rate.rate_rate
                    amount += amt

    data = {
        "year": year,
        "type": type,
        "amount": amount,
    }

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_1_121(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    
    cache_key = f'table-1-121-{type}-{year}'
    serialized_value = redis_client.get(cache_key)
    if serialized_value:
        try:
            data = json.loads(serialized_value.decode('utf-8'))
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            data = None
    else:
        data = None
    
    if not data:
        ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'2','3','4','5','10','13'}))
        organizations_ids = Organizations.objects.values_list(
            'organization_id', flat=True).filter(
            Q(organization_type__in= set(ids)))
        
        

        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        if type == 'budget':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=3)  # budger approved
            )
        if type == 'expenditure':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True) .filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=4)  # expenditure approved
            )
        if type == 'budget':
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(Q(level_code='FS.1'))
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
        
        if type == 'expenditure':
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(Q(level_code='FS.1'))
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_double_count=0)&
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # expenditure approved
            )

        amount = 0
        for item in activities_inputs:
            if type == 'budget':
                if item.activity_input_budget_currency == 'RWF':
                    amount += item.activity_input_budget
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_budget_currency)
                    )
                    if len(rates) == 0:
                        amount += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_budget * rate.rate_rate
                        amount += amt

            if type == 'expenditure':
                if item.activity_input_expenses_currency == 'RWF':
                    amount += item.activity_input_expenses
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_expenses_currency)
                    )
                    if len(rates) == 0:
                        amount += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_expenses * rate.rate_rate
                        amount += amt
            
        data = {
            "year": year,
            "type": type,
            "amount": amount,
        }
        serialized_value = json.dumps(data, cls=DjangoJSONEncoder)
        redis_client.set(cache_key, json.dumps(serialized_value), ex=60*60)  
    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_1_12211(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    cache_key = f'table-1-12211-{type}-{year}'
    serialized_value = redis_client.get(cache_key)
    if serialized_value:
        try:
            data = json.loads(serialized_value.decode('utf-8'))
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            data = None
    else:
        data = None
    if not data:
        ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'4'}))
        organizations_ids = Organizations.objects.values_list(
            'organization_id', flat=True).filter(
            Q(organization_type__in= set(ids)))

        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        

        if type == 'budget':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=3)  # budger approved
            )
            
        if type == 'expenditure':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=4)  # expenditure approved
            )
                

        if type == 'budget':
            levels_ids = Levels.objects.values_list('level_id', flat=True).filter(
                Q(level_code__in={'FS.3', 'FS.4', 'FS.5', 'FS.6', 'FS.7'}))
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
            
        if type == 'expenditure':
            levels_ids = Levels.objects.values_list('level_id', flat=True).filter(
                Q(level_code__in={'FS.3', 'FS.4', 'FS.5', 'FS.6', 'FS.7'}))
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids))&
                Q(activity_input_double_count=0)&
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # expenditure approved
            )
        amount = 0
        for item in activities_inputs:
            if type == 'budget':
                if item.activity_input_budget_currency == 'RWF':
                    amount += item.activity_input_budget
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_budget_currency)
                    )
                    if len(rates) == 0:
                        amount += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_budget * rate.rate_rate
                        amount += amt

            if type == 'expenditure':
                if item.activity_input_expenses_currency == 'RWF':
                    amount += item.activity_input_expenses
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_expenses_currency)
                    )
                    if len(rates) == 0:
                        amount += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_expenses * rate.rate_rate
                        amount += amt

        data = {
            "year": year,
            "type": type,
            "amount": amount,
        }
        serialized_value = json.dumps(data, cls=DjangoJSONEncoder)
        redis_client.set(cache_key, json.dumps(serialized_value), ex=60*60)

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_1_12213(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    cache_key = f'table-1-12213-{type}-{year}'
    serialized_value = redis_client.get(cache_key)
    if serialized_value:
        try:
            data = json.loads(serialized_value.decode('utf-8'))
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            data = None
    else:
        data = None
    if not data:
        ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'1', '12'}))
        organizations_ids = Organizations.objects.values_list(
            'organization_id', flat=True).filter(
            Q(organization_type__in= set(ids)))
        
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        

        if type == 'budget':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=3)  # budger approved
            )
            
        if type == 'expenditure':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=4)  # expenditure approved
            )

        if type == 'budget':
            levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'FS.1', 'FS.2', 'FS.3', 'FS.4', 'FS.5', 'FS.6','FS.7'}))
            excluded_sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'FS.6.1'}))
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            ).exclude(Q(activity_input_funds_transfer_sub_class__in=set(excluded_sub_levels_ids)))


        if type == 'expenditure':
            levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'FS.1', 'FS.2', 'FS.3', 'FS.4', 'FS.5', 'FS.6','FS.7'}))
            excluded_sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'FS.6.1'}))
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_double_count=0)&
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # expenditure approved
            ).exclude(Q(activity_input_funds_transfer_sub_class__in=set(excluded_sub_levels_ids)))

        amount = 0
        for item in activities_inputs:
            if type == 'budget':
                if item.activity_input_budget_currency == 'RWF':
                    amount += item.activity_input_budget
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_budget_currency)
                    )
                    if len(rates) == 0:
                        amount += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_budget * rate.rate_rate
                        amount += amt

            if type == 'expenditure':
                if item.activity_input_expenses_currency == 'RWF':
                    amount += item.activity_input_expenses
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_expenses_currency)
                    )
                    if len(rates) == 0:
                        amount += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_expenses * rate.rate_rate
                        amount += amt

        data = {
            "year": year,
            "type": type,
            "amount": amount,
        }
        serialized_value = json.dumps(data, cls=DjangoJSONEncoder)
        redis_client.set(cache_key, json.dumps(serialized_value), ex=60*60)

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_1_12214(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    cache_key = f'table-1-12214-{type}-{year}'
    serialized_value = redis_client.get(cache_key)
    if serialized_value:
        try:
            data = json.loads(serialized_value.decode('utf-8'))
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            data = None
    else:
        data = None
   
    if not data:
        ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'5', '9', '11','14'}))
        organizations_ids = Organizations.objects.values_list(
            'organization_id', flat=True).filter(
            Q(organization_type__in= set(ids)))
        
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        

        if type == 'budget':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=3)  # budger approved
            )
        if type == 'expenditure':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=4)  # expenditure approved
            )

        if type == 'budget':
            levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'FS.1', 'FS.2', 'FS.3', 'FS.4', 'FS.5', 'FS.6','FS.7'}))
            excluded_sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'FS.6.1'}))
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            ).exclude(Q(activity_input_funds_transfer_sub_class__in=set(excluded_sub_levels_ids)))
        if type == 'expenditure':
            levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'FS.1', 'FS.2', 'FS.3', 'FS.4', 'FS.5', 'FS.6','FS.7'}))
            excluded_sub_levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(Q(level_code__in={'FS.6.1',}))
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_double_count=0)&
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # expenditure approved
            ).exclude(Q(activity_input_funds_transfer_sub_class__in=set(excluded_sub_levels_ids)))

        amount = 0
        for item in activities_inputs:
            if type == 'budget':
                if item.activity_input_budget_currency == 'RWF':
                    amount += item.activity_input_budget
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_budget_currency)
                    )
                    if len(rates) == 0:
                        amount += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_budget * rate.rate_rate
                        amount += amt

            if type == 'expenditure':
                if item.activity_input_expenses_currency == 'RWF':
                    amount += item.activity_input_expenses
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_expenses_currency)
                    )
                    if len(rates) == 0:
                        amount += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_expenses * rate.rate_rate
                        amount += amt

        data = {
            "year": year,
            "type": type,
            "amount": amount,
        }
        serialized_value = json.dumps(data, cls=DjangoJSONEncoder)
        redis_client.set(cache_key, json.dumps(serialized_value), ex=60*60)

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_1_12221(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    cache_key = f'table-1-12221-{type}-{year}'
    serialized_value = redis_client.get(cache_key)
    if serialized_value:
        try:
            data = json.loads(serialized_value.decode('utf-8'))
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            data = None
    else:
        data = None
    if not data:
        ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'1', '12'}))
        organizations_ids = Organizations.objects.values_list(
            'organization_id', flat=True).filter(
            Q(organization_type__in= set(ids)))

        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        

        if type == 'budget':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=3)  # budger approved
            )
            
        if type == 'expenditure':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True) .filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=4)  # expenditure approved
            )

        if type == 'budget':
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(Q(level_code='FS.6.1'))
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_sub_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
        if type == 'expenditure':
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(Q(level_code='FS.6.1'))
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_sub_class__in=set(levels_ids)) &
                Q(activity_input_double_count=0)&
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # expenditure approved
            )

        amount = 0
        for item in activities_inputs:
            if type == 'budget':
                if item.activity_input_budget_currency == 'RWF':
                    amount += item.activity_input_budget
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_budget_currency)
                    )
                    if len(rates) == 0:
                        amount += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_budget * rate.rate_rate
                        amount += amt

            if type == 'expenditure':
                if item.activity_input_expenses_currency == 'RWF':
                    amount += item.activity_input_expenses
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_expenses_currency)
                    )
                    if len(rates) == 0:
                        amount += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_expenses * rate.rate_rate
                        amount += amt

        data = {
            "year": year,
            "type": type,
            "amount": amount,
        }
        serialized_value = json.dumps(data, cls=DjangoJSONEncoder)
        redis_client.set(cache_key, json.dumps(serialized_value), ex=60*60)

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_1_13(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]
    cache_key = f'table-1-13-{type}-{year}'
    serialized_value = redis_client.get(cache_key)
    if serialized_value:
        try:
            data = json.loads(serialized_value.decode('utf-8'))
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            data = None
    else:
        data = None
    if not data:
        if year == "" or year is None:
            return HttpResponseBadRequest("Bad Request", content_type="text/plain")

        organizations_ids = Organizations.objects.values_list(
            'organization_id', flat=True)

        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )

        if type == 'budget':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=3)  # budger approved
            )
        if type == 'expenditure':
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)
                # Q(activity_status=4)  # expenditure approved
            )

        if type == 'budget':
            levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='FS.2'))
            sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='FS.2.1'))
            activities_inputs_1 = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_funds_transfer_sub_class__in=set(sub_levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
            levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='FS.2'))
            sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='FS.2.2'))
            activities_inputs_2 = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_funds_transfer_sub_class__in=set(sub_levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
            levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='FS.7'))
            activities_inputs_3 = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
        if type == 'expenditure':
            levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='FS.2'))
            sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='FS.2.1'))
            activities_inputs_1 = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_funds_transfer_sub_class__in=set(sub_levels_ids)) &
                Q(activity_input_double_count=0)&
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # expenditure approved
            )
            levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='FS.2'))
            sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='FS.2.2'))
            activities_inputs_2 = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_funds_transfer_sub_class__in=set(sub_levels_ids)) &
                Q(activity_input_double_count=0)&
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # expenditure approved
            )
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(Q(level_code='FS.7'))
            activities_inputs_3 = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_double_count=0)&
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # expenditure approved
            )

        amount_1 = 0
        for item in activities_inputs_1:
            if type == 'budget':
                if item.activity_input_budget_currency == 'RWF':
                    amount_1 += item.activity_input_budget
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_budget_currency)
                    )
                    if len(rates) == 0:
                        amount_1 += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_budget * rate.rate_rate
                        amount_1 += amt

            if type == 'expenditure':
                if item.activity_input_expenses_currency == 'RWF':
                    amount_1 += item.activity_input_expenses
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_expenses_currency)
                    )
                    if len(rates) == 0:
                        amount_1 += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_expenses * rate.rate_rate
                        amount_1 += amt

        amount_2 = 0
        for item in activities_inputs_2:
            if type == 'budget':
                if item.activity_input_budget_currency == 'RWF':
                    amount_2 += item.activity_input_budget
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_budget_currency)
                    )
                    if len(rates) == 0:
                        amount_2 += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_budget * rate.rate_rate
                        amount_2 += amt

            if type == 'expenditure':
                if item.activity_input_expenses_currency == 'RWF':
                    amount_2 += item.activity_input_expenses
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_expenses_currency)
                    )
                    if len(rates) == 0:
                        amount_2 += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_expenses * rate.rate_rate
                        amount_2 += amt

        amount_3 = 0
        for item in activities_inputs_3:
            if type == 'budget':
                if item.activity_input_budget_currency == 'RWF':
                    amount_3 += item.activity_input_budget
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_budget_currency)
                    )
                    if len(rates) == 0:
                        amount_3 += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_budget * rate.rate_rate
                        amount_3 += amt

            if type == 'expenditure':
                if item.activity_input_expenses_currency == 'RWF':
                    amount_3 += item.activity_input_expenses
                else:
                    rates = Currency_Rates.objects.filter(
                        Q(rate_fiscal_year=year) &
                        Q(rate_currency=item.activity_input_expenses_currency)
                    )
                    if len(rates) == 0:
                        amount_3 += 0
                    else:
                        rate = rates[0]
                        amt = item.activity_input_expenses * rate.rate_rate
                        amount_3 += amt

        data = {
            "year": year,
            "type": type,
            "amount_1": amount_1,
            "amount_2": amount_2,
            "amount_3": amount_3,
        }
        serialized_value = json.dumps(data, cls=DjangoJSONEncoder)
        redis_client.set(cache_key, json.dumps(serialized_value), ex=60*60)

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_2(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    reported_activities_budget= Activities.objects.filter(Q(activity_status = Activities.STATUS_BUDGET_APPROVED) & Q(activity_fiscal_year = year))
    reported_activities_expenditure= Activities.objects.filter(Q(activity_status = Activities.STATUS_EXPENSES_APPROVED) & Q(activity_fiscal_year = year))
    filtered_organization_budget_ids = reported_activities_budget.values_list('organization_id', flat=True).distinct()
    filtered_organization_expenditure_ids =reported_activities_expenditure.values_list('organization_id', flat=True).distinct()

    if type == "budget":
        ORGANIZATIONS = Organizations.objects.filter(
        Q(organization_id__in= set(filtered_organization_budget_ids))|
        Q(organization_id__in= set(filtered_organization_expenditure_ids))
        )
    if type == "expenditure":
        ORGANIZATIONS = Organizations.objects.filter(
        Q(organization_id__in=filtered_organization_expenditure_ids)
        )

    levels_ids_1 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='1'))
    count_1 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_1))).count()
    

    levels_ids_2 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='2'))
    count_2 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_2))).count()

    levels_ids_3 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='3'))
    count_3 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_3))).count()

    levels_ids_4 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='4'))
    count_4 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_4))).count()

    levels_ids_5 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='5'))
    count_5 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_5))).count()

    levels_ids_6 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='6'))
    count_6 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_6))).count()

    levels_ids_7 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='7'))
    count_7 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_7))).count()

    levels_ids_8 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='8'))
    count_8 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_8))).count()

    levels_ids_9 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='9'))
    count_9 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_9))).count()

    levels_ids_10 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='10'))
    count_10 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_10))).count()

    levels_ids_11 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='11'))
    count_11 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_11))).count()

    levels_ids_12 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='12'))
    count_12 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_12))).count()

    levels_ids_13 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='13'))
    count_13 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_13))).count()

    levels_ids_14 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='14'))
    count_14 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_14))).count()

    levels_ids_15 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='15'))
    count_15 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_15))).count()

    levels_ids_16 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='16'))
    count_16 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_16))).count()

    levels_ids_161 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='16.1'))
    count_161 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_16)) & 
        Q(organization_sub_type__in=set(levels_ids_161))
        ).count()
    
    levels_ids_162 = Levels.objects.values_list(
        'level_id', flat=True).filter(Q(level_code='16.2'))
    count_162 = ORGANIZATIONS.filter(
        Q(organization_type__in=set(levels_ids_16))&
        Q(organization_sub_type__in=set(levels_ids_162))
        ).count()

    data = {
        "year": year,
        "type": type,
        "count_1": count_1,
        "count_2": count_2,
        "count_3": count_3,
        "count_4": count_4,
        "count_5": count_5,
        "count_6": count_6,
        "count_7": count_7,
        "count_8": count_8,
        "count_9": count_9,
        "count_10": count_10,
        "count_11": count_11,
        "count_12": count_12,
        "count_13": count_13,
        "count_14": count_14,
        "count_15": count_15,
        "count_16": count_16,
        "count_161": count_161,
        "count_162": count_162,
    }
    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_3(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    items = []
    parent_levels = Levels.objects.filter(
        Q(level_key='domain', level_parent=0)).order_by('level_code').all()
    for level in parent_levels:
        items.append({
            'id': level.level_id,
            'key': level.level_key,
            'type': 'domain',
            'code': level.level_code,
            'name': level.level_name,
        })
        child_levels = Levels.objects.filter(
            Q(level_key='sub-domain', level_parent=level.level_id)).order_by('level_code').all()
        for level in child_levels:
            items.append({
                'id': level.level_id,
                'key': level.level_key,
                'type': 'sub-domain',
                'code': level.level_code,
                'name': level.level_name,
            })

    data = {
        "year": year,
        "type": type,
        "items": items,
    }

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_4(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    cache_key = f'table-4-{type}-{year}'
    serialized_value = redis_client.get(cache_key)
    if serialized_value:
        try:
            data = json.loads(serialized_value.decode('utf-8'))
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            data = None
    else:
        data = None
    if not data:
        organizations_ids = Organizations.objects.values_list(
            'organization_id', flat=True)

        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        amount_1 = 0
        amount_2 = 0
        amount_3 = 0
        amount_4 = 0
        amount_5 = 0
        amount_6 = 0
        amount_7 = 0
        amount_8 = 0
        if type == 'budget':
            # D.1
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.1') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )

            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
            for item in activities_inputs:
                amount_1 += item.activity_input_budget
            # D.2
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.2') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
            for item in activities_inputs:
                amount_2 += item.activity_input_budget
            # D.3
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.3') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
            for item in activities_inputs:
                amount_3 += item.activity_input_budget
            # D.5
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.5') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
            for item in activities_inputs:
                amount_4 += item.activity_input_budget
            # D.6
            func_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='HC.7'))
            dom_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6')))
            dom_sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6.1')))
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                (Q(activity_domain__in=set(dom_levels_ids))&
                Q(activity_sub_domain__in=set(dom_sub_levels_ids))|
                Q(activity_functions__in = set(func_levels_ids))))
            for item in activities_inputs:
                amount_5 += item.activity_input_budget
            # D.7
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.7') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
            for item in activities_inputs:
                amount_6 += item.activity_input_budget
            # D.8
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.8') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
            for item in activities_inputs:
                amount_7 += item.activity_input_budget
            # D.9
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.9') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
            )
            for item in activities_inputs:
                amount_8 += item.activity_input_budget
        if type == 'expenditure':
            # D.1
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.1') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_double_count=0)&
                #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_status= Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
            )
            for item in activities_inputs:
                amount_1 += item.activity_input_expenses
            # D.2
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.2') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_double_count=0)&
                #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
            )
            for item in activities_inputs:
                amount_2 += item.activity_input_expenses
            # D.3
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.3') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_double_count=0)&
            # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
            )
            for item in activities_inputs:
                amount_3 += item.activity_input_expenses
            # D.5
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.5') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_double_count=0)&
            # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
            )
            for item in activities_inputs:
                amount_4 += item.activity_input_expenses
            # D.6
            func_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='HC.7'))
            dom_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6')))
            dom_sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6.1')))
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                (Q(activity_domain__in=set(dom_levels_ids))&
                Q(activity_sub_domain__in=set(dom_sub_levels_ids))|
                Q(activity_functions__in = set(func_levels_ids))))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_double_count=0)&
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
            )
            for item in activities_inputs:
                amount_5 += item.activity_input_expenses
            # D.7
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.7') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )

            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_double_count=0)&
                #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
            )
            for item in activities_inputs:
                amount_6 += item.activity_input_expenses
            # D.8
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.8') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )

            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_double_count=0)&
                #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
            )
            for item in activities_inputs:
                amount_7 += item.activity_input_expenses
            # D.9
            levels_ids = Levels.objects.values_list(
                'level_id', flat=True).filter(
                Q(level_code='D.9') & (
                    Q(level_key='domain') | Q(level_key='sub-domain'))
            )
            activities_ids = Activities.objects.values_list(
                'activity_id', flat=True).filter(
                Q(project_id__in=set(projects_ids)) &
                Q(activity_fiscal_year=year)&
                Q(activity_domain__in=set(levels_ids)))
            
            activities_inputs = Activities_Inputs.objects.filter(
                Q(activity_id__in=set(activities_ids)) &
                Q(activity_input_double_count=0)&
                #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
                Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
            )
            for item in activities_inputs:
                amount_8 += item.activity_input_expenses

        data = {
            "year": year,
            "type": type,
            "amount_1": amount_1,
            "amount_2": amount_2,
            "amount_3": amount_3,
            "amount_4": amount_4,
            "amount_5": amount_5,
            "amount_6": amount_6,
            "amount_7": amount_7,
            "amount_8": amount_8,
        }
        serialized_value = json.dumps(data, cls=DjangoJSONEncoder)
        redis_client.set(cache_key, json.dumps(serialized_value), ex=60*30)

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_5(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    

    organizations_ids = Organizations.objects.values_list(
        'organization_id', flat=True)
    projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
        Q(organization_id__in=set(organizations_ids))
    )

    amount_1 = 0
    amount_2 = 0
    amount_3 = 0
    amount_4 = 0
    amount_5 = 0
    amount_6 = 0
    if type == 'budget':
        # HC.1
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.1')
        )

        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_1 += item.activity_input_budget
        # HC.2
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.2')
        )
    
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_2 += item.activity_input_budget
    # HC.3
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.3')
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_3 += item.activity_input_budget
        # HC.4
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.4')
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
        (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_4 += item.activity_input_budget
        # HC.5
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.5')
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
        (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_5 += item.activity_input_budget
        # HC.6
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.6')
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_6 += item.activity_input_budget
    if type == 'expenditure':
        # HC.1
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.1')
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0)&
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status= Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_1 += item.activity_input_expenses
        # HC.2
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.2')
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0)&
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_2 += item.activity_input_expenses
        # HC.3
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.3')
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0)&
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_3 += item.activity_input_expenses
        # HC.4
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.4')
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0)&
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_4 += item.activity_input_expenses
        # HC.5
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.5')
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0)&
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_5 += item.activity_input_expenses
    # HC.6
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='HC.6')
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_functions__in=set(levels_ids)))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0)&
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_6 += item.activity_input_expenses

    data = {
        "year": year,
        "type": type,
        "amount_1": amount_1,
        "amount_2": amount_2,
        "amount_3": amount_3,
        "amount_4": amount_4,
        "amount_5": amount_5,
        "amount_6": amount_6,
    }

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_6_public(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    
    ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'2', '3', '4','10','13'}))
    organizations_ids = Organizations.objects.values_list(
        'organization_id', flat=True).filter(
        Q(organization_type__in= set(ids)))

    projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
        Q(organization_id__in=set(organizations_ids))
    )

    amount_1 = 0
    amount_2 = 0
    amount_3 = 0
    amount_4 = 0
    amount_5 = 0
    amount_6 = 0
    amount_7 = 0
    amount_8 = 0
    if type == 'budget':
        # D.1
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.1') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_1 += item.activity_input_budget
        # D.2
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.2') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_2 += item.activity_input_budget
        # D.3
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.3') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_3 += item.activity_input_budget
        # D.5
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.5') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_4 += item.activity_input_budget
        # D.6

        func_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='HC.7'))
        dom_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6')))
        dom_sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6.1')))

        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            (Q(activity_domain__in=set(dom_levels_ids))&
            Q(activity_sub_domain__in=set(dom_sub_levels_ids))|
            Q(activity_functions__in = set(func_levels_ids))))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            # (Q(activity_input_funds_transfer_class__in=set(levels_ids))|
            #  Q(activity_input_funds_transfer_sub_class__in=set(sub_levels_ids))) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_5 += item.activity_input_budget
        # D.7
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.7') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_6 += item.activity_input_budget
        # D.8
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.8') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_7 += item.activity_input_budget
        # D.9
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.9') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )

        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_8 += item.activity_input_budget
    if type == 'expenditure':
        # D.1
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.1') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_1 += item.activity_input_expenses
        # D.2
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.2') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_2 += item.activity_input_expenses
        # D.3
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.3') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_3 += item.activity_input_expenses
        # D.5
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.5') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_4 += item.activity_input_expenses
        # D.6

        func_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='HC.7'))
        dom_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6')))
        dom_sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6.1')))

        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            (Q(activity_domain__in=set(dom_levels_ids))&
            Q(activity_sub_domain__in=set(dom_sub_levels_ids))|
            Q(activity_functions__in = set(func_levels_ids))))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            # (Q(activity_input_funds_transfer_class__in=set(levels_ids))|
            # Q(activity_input_funds_transfer_sub_class__in=set(sub_levels_ids)))&
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_5 += item.activity_input_expenses
        # D.7
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.7') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_6 += item.activity_input_expenses
        # D.8
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.8') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_7 += item.activity_input_expenses
        # D.9
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.9') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_8 += item.activity_input_expenses

    data = {
        "year": year,
        "type": type,
        "amount_1": amount_1,
        "amount_2": amount_2,
        "amount_3": amount_3,
        "amount_4": amount_4,
        "amount_5": amount_5,
        "amount_6": amount_6,
        "amount_7": amount_7,
        "amount_8": amount_8,
    }

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_6_private(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'1', '5', '6','7','11','12','14'}))
    organizations_ids = Organizations.objects.values_list(
        'organization_id', flat=True).filter(
        Q(organization_type__in= set(ids)))

    projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
        Q(organization_id__in=set(organizations_ids))
    )
    amount_1 = 0
    amount_2 = 0
    amount_3 = 0
    amount_4 = 0
    amount_5 = 0
    amount_6 = 0
    amount_7 = 0
    amount_8 = 0
    if type == 'budget':
        # D.1
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.1') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_1 += item.activity_input_budget
        # D.2
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.2') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_2 += item.activity_input_budget
        # D.3
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.3') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_3 += item.activity_input_budget
        # D.5
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.5') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )

        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_4 += item.activity_input_budget
        # D.6

        func_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='HC.7'))
        dom_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6')))
        dom_sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6.1')))
        
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            (Q(activity_domain__in=set(dom_levels_ids))&
            Q(activity_sub_domain__in=set(dom_sub_levels_ids))|
            Q(activity_functions__in = set(func_levels_ids))))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            # (Q(activity_input_funds_transfer_class__in=set(levels_ids))|
            #  Q(activity_input_funds_transfer_sub_class__in=set(sub_levels_ids))) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_5 += item.activity_input_budget
        # D.7
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.7') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
        (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_6 += item.activity_input_budget
        # D.8
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.8') & (
                Q(level_key='domain') | Q(level_key='sub-domain')))
        
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_7 += item.activity_input_budget
        # D.9
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.9') & (
                Q(level_key='domain') | Q(level_key='sub-domain')))
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_8 += item.activity_input_budget
    if type == 'expenditure':
        # D.1
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.1') & (
                Q(level_key='domain') | Q(level_key='sub-domain')))
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status= Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_1 += item.activity_input_expenses
        # D.2
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.2') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_2 += item.activity_input_expenses
        # D.3
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.3') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_3 += item.activity_input_expenses
        # D.5
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.5') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_4 += item.activity_input_expenses
        # D.6
        func_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='HC.7'))
        dom_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6')))
        dom_sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6.1')))
        
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            (Q(activity_domain__in=set(dom_levels_ids))&
            Q(activity_sub_domain__in=set(dom_sub_levels_ids))|
            Q(activity_functions__in = set(func_levels_ids))))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_5 += item.activity_input_expenses
        # D.7
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.7') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_6 += item.activity_input_expenses
        # D.8
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.8') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_7 += item.activity_input_expenses
        # D.9
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.9') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )

        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_8 += item.activity_input_expenses

    data = {
        "year": year,
        "type": type,
        "amount_1": amount_1,
        "amount_2": amount_2,
        "amount_3": amount_3,
        "amount_4": amount_4,
        "amount_5": amount_5,
        "amount_6": amount_6,
        "amount_7": amount_7,
        "amount_8": amount_8,
    }

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_6_external(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
   
    ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code__in={'15', '16'}))
    organizations_ids = Organizations.objects.values_list(
        'organization_id', flat=True).filter(
        Q(organization_type__in= set(ids)))

    projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
        Q(organization_id__in=set(organizations_ids))
    )
    amount_1 = 0
    amount_2 = 0
    amount_3 = 0
    amount_4 = 0
    amount_5 = 0
    amount_6 = 0
    amount_7 = 0
    amount_8 = 0
    if type == 'budget':
        # D.1
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.1') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )

        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_1 += item.activity_input_budget
        # D.2
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.2') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_2 += item.activity_input_budget
        # D.3
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.3') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_3 += item.activity_input_budget
        # D.5
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.5') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_4 += item.activity_input_budget
        # D.6
        func_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='HC.7'))
        dom_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6')))
        dom_sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6.1')))
        
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            (Q(activity_domain__in=set(dom_levels_ids))&
            Q(activity_sub_domain__in=set(dom_sub_levels_ids))|
            Q(activity_functions__in = set(func_levels_ids))))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_5 += item.activity_input_budget
        # D.7
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.7') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_6 += item.activity_input_budget
        # D.8
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.8') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_7 += item.activity_input_budget
        # D.9
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.9') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_8 += item.activity_input_budget
    if type == 'expenditure':
        # D.1
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.1') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_1 += item.activity_input_expenses
        # D.2
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.2') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_2 += item.activity_input_expenses
        # D.3
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.3') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_3 += item.activity_input_expenses
        # D.5
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.5') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_4 += item.activity_input_expenses
        # D.6
        func_levels_ids = Levels.objects.values_list('level_id', flat=True).filter(Q(level_code='HC.7'))
        dom_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6')))
        dom_sub_levels_ids = Levels.objects.values_list('level_id', flat=True).filter((Q(level_code='D.6.1')))
        
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            (Q(activity_domain__in=set(dom_levels_ids))&
            Q(activity_sub_domain__in=set(dom_sub_levels_ids))|
            Q(activity_functions__in = set(func_levels_ids))))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_5 += item.activity_input_expenses
        # D.7
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.7') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_6 += item.activity_input_expenses
        # D.8
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.8') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_7 += item.activity_input_expenses
        # D.9
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='D.9') & (
                Q(level_key='domain') | Q(level_key='sub-domain'))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)&
            Q(activity_domain__in=set(levels_ids)))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_8 += item.activity_input_expenses

    data = {
        "year": year,
        "type": type,
        "amount_1": amount_1,
        "amount_2": amount_2,
        "amount_3": amount_3,
        "amount_4": amount_4,
        "amount_5": amount_5,
        "amount_6": amount_6,
        "amount_7": amount_7,
        "amount_8": amount_8,
    }

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


@csrf_exempt
def get_table_9(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")
    year = request.POST["year"]
    type = request.POST["type"]

    if year == "" or year is None:
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
   
    amount_1 = 0
    amount_2 = 0
    amount_3 = 0
    amount_4 = 0
    amount_5 = 0
    amount_6 = 0
    amount_7 = 0
    amount_8 = 0
    amount_9 = 0
    amount_10 = 0
    amount_11 = 0
    amount_12 = 0
    amount_13 = 0
    amount_14 = 0
    amount_15 = 0
    amount_16 = 0
    if type == 'budget':
        # 1
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='1')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )

        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )

        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_1 += item.activity_input_budget
        # 2
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='2')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )

        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )

        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_2 += item.activity_input_budget
        # 3
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='3')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )

        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )

        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_3 += item.activity_input_budget
        # 4
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='4')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )

        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )

        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_4 += item.activity_input_budget
        # 5
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='5')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_5 += item.activity_input_budget
        # 6
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='6')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_6 += item.activity_input_budget
        # 7
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='7')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_7 += item.activity_input_budget
        # 8
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='8')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_8 += item.activity_input_budget
        # 9
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='9')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_9 += item.activity_input_budget
        # 10
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='10')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_10 += item.activity_input_budget
        # 11
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='11')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_11 += item.activity_input_budget
        # 12
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='12')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year)) 
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
        (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_12 += item.activity_input_budget
        # 13
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='13')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_13 += item.activity_input_budget
        # 14
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='14')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_14 += item.activity_input_budget
        # 15
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='15')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_15 += item.activity_input_budget
        # 16
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='16')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
        )
        for item in activities_inputs:
            amount_16 += item.activity_input_budget
    if type == 'expenditure':
        # 1
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='1')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_1 += item.activity_input_expenses
        # 2
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='2')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_2 += item.activity_input_expenses
        # 3
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='3')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_3 += item.activity_input_expenses
        # 4
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='4')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_4 += item.activity_input_expenses
        # 5
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='5')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_5 += item.activity_input_expenses
        # 6
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='6')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_6 += item.activity_input_expenses
        # 7
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='7')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_7 += item.activity_input_expenses
        # 8
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='8')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_8 += item.activity_input_expenses
        # 9
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='9')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
        #  Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_9 += item.activity_input_expenses
        # 10
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='10')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_10 += item.activity_input_expenses
        # 11
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='11')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_11 += item.activity_input_expenses
        # 12
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='12')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_12 += item.activity_input_expenses
        # 13
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='13')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED) 
        )
        for item in activities_inputs:
            amount_13 += item.activity_input_expenses
        # 14
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='14')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_14 += item.activity_input_expenses
        # 15
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='15')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
            #Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_15 += item.activity_input_expenses
        # 16
        levels_ids = Levels.objects.values_list(
            'level_id', flat=True).filter(
            Q(level_code='16')
        )
        organizations_ids = Organizations.objects.values_list('organization_id', flat=True).filter(
            Q(organization_type__in =set(levels_ids))
        )
        projects_ids = Projects.objects.values_list('project_id', flat=True).filter(
            Q(organization_id__in=set(organizations_ids))
        )
        activities_ids = Activities.objects.values_list(
            'activity_id', flat=True).filter(
            Q(project_id__in=set(projects_ids)) &
            Q(activity_fiscal_year=year))
        activities_inputs = Activities_Inputs.objects.filter(
            Q(activity_id__in=set(activities_ids)) &
            Q(activity_input_double_count=0) &
        # Q(activity_input_funds_transfer_class__in=set(levels_ids)) &
            Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # budger approved
        )
        for item in activities_inputs:
            amount_16 += item.activity_input_expenses

    data = {
        "year": year,
        "type": type,
        "amount_1": amount_1,
        "amount_2": amount_2,
        "amount_3": amount_3,
        "amount_4": amount_4,
        "amount_5": amount_5,
        "amount_6": amount_6,
        "amount_7": amount_7,
        "amount_8": amount_8,
        "amount_9": amount_9,
        "amount_10": amount_10,
        "amount_11": amount_11,
        "amount_12": amount_12,
        "amount_13": amount_13,
        "amount_14": amount_14,
        "amount_15": amount_15,
        "amount_16": amount_16,
        "amount": amount_1 + amount_2 + amount_3 + amount_4 + amount_5 + amount_6 + amount_7 + amount_8 + amount_9 + amount_10 + amount_11 + amount_12 + amount_13 + amount_14 + amount_15 + amount_16,
    }

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )

# def get_total_budget_expenditure(request):
#         for item in Gdp_Populations.objects.all():
#             year = item.fiscal_year
#             total_budget = 0
#             total_expenses = 0
#             activities_ids = Activities.objects.values_list(
#                     'activity_id', flat=True) .filter(
#                     Q(activity_fiscal_year=year)
#                 )
            
#             #budget
#             activities_inputs_budget = Activities_Inputs.objects.filter(
#                     Q(activity_id__in=set(activities_ids)) &
#                     (Q(activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED)|
#                     Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)| 
#                     Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED))# budger approved
#                 )
           
#             for input in activities_inputs_budget:
#                 if input.activity_input_budget_currency == 'RWF':
#                     total_budget += input.activity_input_budget
#                 else:
#                     rates = Currency_Rates.objects.filter(
#                         Q(rate_fiscal_year=year) &
#                         Q(rate_currency=input.activity_input_budget_currency)
#                     )
#                     if len(rates) == 0:
#                         total_budget += 0
#                     else:
#                         rate = rates[0]
#                         amt = input.activity_input_budget * rate.rate_rate
#                         total_budget += amt
           
#             Methods_Gdp_Populations.update_total_budget(request,total_budget,item)


#             activities_inputs_expenses = Activities_Inputs.objects.filter(
#                 Q(activity_id__in=set(activities_ids)) &
#                 Q(activity_input_double_count=0) &
#                 Q(activity_input_status=Activities_Inputs.STATUS_EXPENSES_APPROVED)  # expenditure approved
#             )
#             for input in activities_inputs_expenses:
#                 if input.activity_input_expenses_currency == 'RWF':
#                     total_expenses += input.activity_input_expenses
#                 else:
#                     rates = Currency_Rates.objects.filter(
#                         Q(rate_fiscal_year=year) &
#                         Q(rate_currency=input.activity_input_expenses_currency)
#                     )
#                     if len(rates) == 0:
#                         total_budget += 0
#                     else:
#                         rate = rates[0]
#                         amt = input.activity_input_expenses * rate.rate_rate
#                         total_expenses += amt
#             item.expenditure = total_expenses 
#             Methods_Gdp_Populations.update_total_expenditure(request,total_expenses,item) 