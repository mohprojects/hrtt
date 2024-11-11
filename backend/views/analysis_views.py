import io
import pandas as pd
from django.db import connection
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

from app.utils import Utils
from django.db.models import Q
from app import settings
from app.models.users import Users
from app.models.users import Users
from app.models.organizations import Organizations
from app.models.projects import Projects
from app.models.activities import Activities
from app.models.activities_inputs import Activities_Inputs
from app.models.levels import Levels

from app.models.methods.users import Methods_Users

from celery import shared_task
from celery.result import AsyncResult




def index(request):
    template_url = "analysis/index.html"
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
            "section": settings.BACKEND_SECTION_ANALYSIS,
            "title": 'Analysis',
            "name": 'Analysis',
            "user": user,
            "fiscal_year_choices":fiscal_year_choices,
             "auth_permissions": auth_permissions,
            "index_url": reverse("analysis_index"),
        },
    )
    
    
@csrf_exempt
def get_data_for_analysis(request): 
    fiscal_years = request.GET.getlist('years[]')
    base_query = """
        SELECT
        ot.level_code AS organization_type_code,
        ot.level_name AS organization_type_name,
        o.organization_name,
        p.project_name,
        a.activity_name,
        CASE 
            WHEN a.activity_domain = 0 THEN 0
            ELSE ad.level_code
        END AS domain_of_intervention_code,
        CASE 
            WHEN a.activity_domain = 0 THEN '0'
            ELSE ad.level_name
        END AS domain_of_intervention_name,
        CASE 
            WHEN a.activity_sub_domain = 0 THEN 0
            ELSE asd.level_code
        END AS sub_domain_of_intervention_code,
        CASE 
            WHEN a.activity_sub_domain = 0 THEN '0'
            ELSE asd.level_name
        END AS sub_domain_of_intervention_name,
        CASE 
            WHEN a.activity_functions = 0 THEN '0'
            ELSE af.level_name
        END AS function_name,
        CASE 
            WHEN a.activity_location = 0 THEN '0'
            ELSE al.level_name
        END AS location_name,
        a.activity_fiscal_year AS fy,
        CASE 
            WHEN ai.activity_input_class = 0 THEN 0
            ELSE ic.level_code
        END AS input_code,
        CASE 
            WHEN ai.activity_input_class = 0 THEN '0'
            ELSE ic.level_name
        END AS input,
        CASE 
            WHEN ai.activity_input_sub_class = 0 THEN 0
            ELSE isc.level_code
        END AS input_sub_class_code,
        CASE 
            WHEN ai.activity_input_sub_class = 0 THEN '0'
            ELSE isc.level_name
        END AS input_sub_class_name,
        CASE 
            WHEN ai.activity_input_scheme_class = 0 THEN 0
            ELSE fsc.level_code
        END AS financing_scheme_code,
        CASE 
            WHEN ai.activity_input_scheme_class = 0 THEN '0'
            ELSE fsc.level_name
        END AS financing_scheme_name,
        CASE 
            WHEN ai.activity_input_scheme_sub_class = 0 THEN 0
            ELSE fssc.level_code
        END AS financing_scheme_sub_class_code,
        CASE 
            WHEN ai.activity_input_scheme_sub_class = 0 THEN '0'
            ELSE fssc.level_name
        END AS financing_scheme_sub_class_name,
        CASE 
            WHEN ai.activity_input_funds_transfer_class = 0 THEN 0
            ELSE fs.level_code
        END AS financing_source_code,
        CASE 
            WHEN ai.activity_input_funds_transfer_class = 0 THEN '0'
            ELSE fs.level_name
        END AS financing_source_name,
        CASE 
            WHEN ai.activity_input_funds_transfer_sub_class = 0 THEN 0
            ELSE fss.level_code
        END AS financing_source_sub_code,
        CASE 
            WHEN ai.activity_input_funds_transfer_sub_class = 0 THEN '0'
            ELSE fss.level_name
        END AS financing_source_sub_name,
        CASE 
            WHEN ai.activity_input_funder = 0 THEN '0'
            ELSE funder.organization_name
        END AS activity_input_funder,
        CASE 
            WHEN LEFT(ai.activity_input_implementer, 5) = 'impl_' THEN impl.implementer_name
            ELSE org_impl.organization_name 
        END AS activity_input_implementer,
        
        ai.activity_input_expenses AS Expenditure_Amount,
        ai.activity_input_expenses_currency AS Currency,
        CASE 
            WHEN ai.activity_input_double_count = 0 THEN 'No'
            ELSE 'Yes'
        END AS Double_count
        
    FROM 
        app_activities_inputs ai
    JOIN 
        app_activities a ON ai.activity_id = a.activity_id
    JOIN 
        app_projects p ON a.project_id = p.project_id
    JOIN 
        app_organizations o ON p.organization_id = o.organization_id
    LEFT JOIN 
        app_levels ot ON o.organization_type = ot.level_id
    LEFT JOIN 
        app_levels ad ON a.activity_domain = ad.level_id
    LEFT JOIN 
        app_levels asd ON a.activity_sub_domain = asd.level_id
    LEFT JOIN 
        app_levels af ON a.activity_functions = af.level_id
    LEFT JOIN 
        app_levels al ON a.activity_location = al.level_id
    LEFT JOIN 
        app_levels ic ON ai.activity_input_class = ic.level_id
    LEFT JOIN 
        app_levels isc ON ai.activity_input_sub_class = isc.level_id
    LEFT JOIN 
        app_levels fsc ON ai.activity_input_scheme_class = fsc.level_id
    LEFT JOIN 
        app_levels fssc ON ai.activity_input_scheme_sub_class = fssc.level_id
    LEFT JOIN 
        app_levels fs ON ai.activity_input_funds_transfer_class = fs.level_id
    LEFT JOIN 
        app_levels fss ON ai.activity_input_funds_transfer_sub_class = fss.level_id
    LEFT JOIN 
        app_organizations funder ON ai.activity_input_funder = funder.organization_id
    LEFT JOIN
        app_implementers impl ON ai.activity_input_implementer = impl.implementer_id
    LEFT JOIN 
        app_organizations org_impl ON ai.activity_input_implementer = org_impl.organization_id
    """
    data = []
    if fiscal_years:
        fiscal_years_placeholder = ', '.join(['%s'] * len(fiscal_years))
        query = base_query + f" WHERE a.activity_fiscal_year IN ({fiscal_years_placeholder})"
        params = fiscal_years
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]  
    return JsonResponse({'success': True, 'data': data}, safe=False)
    
