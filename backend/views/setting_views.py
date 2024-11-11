import io
import  json
import pandas as pd
from django.contrib import messages
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    JsonResponse
)
from django.db import connection

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q
from app import settings
from app.models.users import Users
from app.models.methods.users import Methods_Users
from app.utils import Utils
from app.models.methods.mongo import Methods_Mongo
from app.models.organizations import Organizations
from app.models.projects import Projects
from app.models.activities import Activities
from app.models.activities_inputs import Activities_Inputs
from app.models.levels import Levels
from app.models.implementers import Implementers

from app.models.methods.organizations import Methods_Organizations
from app.models.methods.projects import Methods_Projects
from app.models.methods.implementers import Methods_Implementers
from app.models.methods.activities import Methods_Activities
from app.models.methods.activities_inputs import Methods_Activities_Inputs
from app.map_ifmis_to_hrtt import hrtt_inputs_factory


@csrf_exempt
def temp_upload(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    else:
        if request.POST:
            file_path = settings.MEDIA_ROOT + "/temp/" + request.POST["name"]
            image_data = request.POST["data"]
            Utils.save_image_base64(image_data, file_path)
            return HttpResponse("success")
        else:
            return HttpResponseBadRequest("no data")


@csrf_exempt
def generate_qr_code(data, size=10, border=0):
    print("QR Data: " + data)
    import qrcode

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image()


@csrf_exempt
def get_qr_code_image(request, size, text):
    print(size)
    print(text)
    qr = generate_qr_code(text, 10, 2)
    response = HttpResponse()
    qr.save(response, "PNG")
    return response

fiscal_year_choices = Utils.get_fiscal_year_choices_for_system_report()

def index(request):
    template_url = "settings/index.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    else:
        auth_permissions = Methods_Users.get_auth_permissions(user)
        return render(
            request,
            template_url,
            {
                "section": settings.BACKEND_SECTION_SETTINGS,
                "title": "Settings",
                "name": "settings",
                "user": user,
                "auth_permissions": auth_permissions,
                "fiscal_year_choices":fiscal_year_choices,
            },
        )


def update_database(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    else:
        Methods_Users.get_auth_permissions(user)

        # messages.success(request, 'Updated successfully.')
        return redirect(reverse("settings_index"))


def reset_database(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    else:
        Methods_Users.get_auth_permissions(user)

        from django.db import connection

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE `app`")

        cursor = Methods_Mongo.get_collection(settings.MODEL_LOGS).drop()
        cursor = Methods_Mongo.get_collection(settings.MODEL_SMS_LOGS).drop()
        cursor = Methods_Mongo.get_collection(settings.MODEL_EMAIL_LOGS).drop()
        cursor = Methods_Mongo.get_collection(settings.MODEL_NOTIFICATIONS).drop()

        messages.success(request, "Reset database successfully.")
        return redirect(reverse("settings_index"))


def clear_logs(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    else:
        Methods_Users.get_auth_permissions(user)

        from django.db import connection

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE `failed_login`")
        cursor.execute("TRUNCATE TABLE `django_session`")
        cursor.execute("TRUNCATE TABLE `django_db_logger_statuslog`")

        messages.success(request, "Cleared logs successfully.")
        return redirect(reverse("settings_index"))


def reset_users(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    else:
        Methods_Users.get_auth_permissions(user)

        messages.success(request, "Reset users successfully.")
        return redirect(reverse("settings_index"))


def import_excel(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    else:
        Methods_Users.get_auth_permissions(user)
        return HttpResponseNotFound("Not Found", content_type="text/plain")

def clean_decimal_string(decimal_string):
    # Remove non-numeric characters and spaces
    cleaned_string = ''.join(char for char in decimal_string if char.isdigit() or char == '.')
    return cleaned_string

def save_data(request, user,  
              organization_name='',
              organization_type_code='',
              double_count='',
              project_name='',
              funder_name='',
              fa_code='',
              fa_sub_code='',
              implementer_name='',
              activity_name='',
              location_name='',
              domain_code='',
              sub_domain_code='',
              function_name='',
              care_provider_class='',
              care_provider_sub_class='',
              input_code='',
              input_sub_code='',
              fsc_fs_code='',
              fsc_fs_sub_code='',
              expenditure='0.0',
              fiscal_year=''):
    sub_domain = 0
    scheme_class = 0
    scheme_sub_class = 0
    transfer_class = 0
    transfer_sub_class = 0
    double_counted  = 0
    funder_id = 0
    implementer_id = 0
    project_data = {}
    activities_data = {}
    activity = None
    activities_inputs_data = {}
    
           
                
    if organization_type_code:
        try:
            organization_type = Levels.objects.get(Q(level_code = int(organization_type_code)) & Q(level_key__icontains ='organization-type'))
            organization_type = organization_type.level_id
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            organization_type = 0
            
    if organization_name and isinstance(organization_name, str):
        organization_name= organization_name.strip().title()
        try:
            organization = Organizations.objects.get(Q(organization_name=organization_name))
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist): 
            organization_data = {
                "name":organization_name,
                "email": "fill@email.com",
                "phone_number": "0000000000",
                "type": organization_type,
                "category": 0,
                "financial_agent_class":0,
                "financial_agent_sub_class": 0,
                "financial_schemes_name": 0,
                "financial_schemes_class": 0,
                "financial_schemes_sub_class":0,
                "healthcare_class":0,
                "healthcare_sub_class":0,
                "sub_type":0,
            }
            err, msg, organization = Methods_Organizations.create(request, user, organization_data)
            
    if project_name and isinstance(project_name, str):
        project_name= project_name.strip().title()
        try:
            project = Projects.objects.get(project_name = project_name, organization_id = organization.organization_id)
        except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
            project_data["name"] = project_name
            project_data["financing_agent"] = "[]"
            project_data["implementer"] = "[]"
            project_data["organization_id"] = organization.organization_id
            project_err, project_msg, project = Methods_Projects.create(request, user,project_data)
    
    if implementer_name and isinstance(implementer_name, str): 
        implementer_name = implementer_name.strip().title()   
        try:
            implementer = Organizations.objects.get(Q(organization_name= implementer_name))
            implementer_id = implementer.organization_id
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist): 
            implementer = None
            
        if not implementer:
            try:
                implementer = Implementers.objects.get(Q(implementer_name=implementer_name.strip().title() ))
                implementer_id = f'impl_{implementer.implementer_id}'
            except (TypeError, ValueError, OverflowError, Implementers.DoesNotExist):
                implementer_data = {
                    "name": implementer_name,
                }
                implementer_err, implementer_msg, implementer = Methods_Implementers.create(request, user, implementer_data)
                implementer_id = f'impl_{implementer.implementer_id}'
             
    
    if fa_code and isinstance(fa_code, str):
        try:
            financing_agent_class = Levels.objects.get(Q(level_code =fa_code) & Q(level_key ='financing-agent-type')) 
            financing_agent_class  = financing_agent_class.level_id
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            financing_agent_class  = 0
            
    if fa_sub_code and isinstance(fa_sub_code, str):    
        try:
            financing_agent_sub_class = Levels.objects.get(Q(level_code = fa_sub_code) & Q(level_key ='financing-agent-type')) 
            financing_agent_sub_class  = financing_agent_sub_class.level_id
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            financing_agent_sub_class  = 0
    if funder_name and isinstance(funder_name, str):
        funder_name = funder_name.strip().title()
        try:
            funder = Organizations.objects.get(Q(organization_name=funder_name))
            funder_id = funder.organization_id
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            funder_id = 0 
                
    if fsc_fs_code and isinstance(fsc_fs_code, str) :
        if "HF" in fsc_fs_code:
            try:
                scheme_class = Levels.objects.get(Q(level_code = fsc_fs_code ) & Q(level_key ='financing-scheme-type') )
                scheme_class = scheme_class.level_id
            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                scheme_class = 0
        if "FS" in fsc_fs_code:
            try:
                transfer_class = Levels.objects.get(Q(level_code = fsc_fs_code ) & Q(level_key ='financing-source-type') )
                transfer_class =  transfer_class.level_id
            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                transfer_class = 0
            
    if fsc_fs_sub_code and isinstance(fsc_fs_sub_code, str):
        if "HF" in fsc_fs_sub_code:   
            try:
                scheme_sub_class = Levels.objects.get(Q(level_code = fsc_fs_sub_code) & Q(level_key ='financing-scheme-type'))
                scheme_sub_class = scheme_sub_class.level_id
            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                scheme_sub_class = 0
                
        if "FS" in fsc_fs_sub_code:
            try:
                transfer_sub_class = Levels.objects.get(Q(level_code = fsc_fs_sub_code ) & Q(level_key ='financing-source-type') )
                transfer_sub_class =  transfer_sub_class.level_id
            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                transfer_class = 0
    if domain_code and isinstance(domain_code, str):    
        try:
            domain = Levels.objects.get(Q(level_code=domain_code) & Q(level_key='domain') )
            domain = domain.level_id
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            domain = 0
            
    if sub_domain_code:
        try:
            sub_domain = Levels.objects.get(Q(level_code= sub_domain_code) & Q(level_key ='sub-domain') )
            sub_domain = sub_domain.level_id
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            sub_domain = 0
            
    if function_name and isinstance(function_name, str):    
        try:
            function = Levels.objects.get(Q(level_name__contains= function_name) & Q(level_key ='function') & Q(level_parent = sub_domain))
            function  = function.level_id
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            function = 0
            
    if care_provider_class and isinstance(care_provider_class,str):    
        try:
            health_care_provider_class = Levels.objects.get(Q(level_code= care_provider_class) & Q(level_key ='health-provider-type'))
            health_care_provider_class  = health_care_provider_class.level_id
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            health_care_provider_class = 0
    if care_provider_sub_class and isinstance(care_provider_sub_class,str):    
        try:
            health_care_provider_sub_class = Levels.objects.get(Q(level_code= care_provider_sub_class) & Q(level_key ='health-provider-type'))
            health_care_provider_sub_class  = health_care_provider_sub_class.level_id
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            health_care_provider_sub_class = 0
            
    if location_name and isinstance(location_name, str):    
        try:
            location = Levels.objects.get(Q(level_name = location_name) & Q(level_key__icontains ='location'))
            location = location.level_id
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            location = 0
    if input_code and isinstance(input_code,str):    
        try:
            input_class = Levels.objects.get(Q(level_code =input_code) & Q(level_key ='inputs'))
            input_class = input_class .level_id
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            input_class = 0
    if input_sub_code and isinstance(input_sub_code,str):    
        try:
            input_sub_class = Levels.objects.get(Q(level_code =input_sub_code) & Q(level_key ='inputs') & Q(level_parent =input_class))
            input_sub_class = input_sub_class.level_id
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            input_sub_class = 0 
    
    if double_count == "Yes":
        double_counted = 1
    
    if activity_name and isinstance(activity_name, str):    
        activities_data["name"] = activity_name
        activities_data["organization_id"] = organization.organization_id
        activities_data["project_id"] =  project.project_id
        activities_data["location"] =  location
        activities_data["domain"] =  domain
        activities_data["sub_domain"] =  sub_domain
        activities_data["functions"] =  function
        activities_data["fiscal_year"] = fiscal_year 
        activities_data["status"] = Activities.STATUS_EXPENSES_APPROVED
        activity_err, activity_msg, activity = Methods_Activities.create(request, user,activities_data)
        
    if activity :
        activities_inputs_data["activity_id"] = activity.activity_id
        activities_inputs_data["input_class"] = input_class
        activities_inputs_data["input_sub_class"] =input_sub_class
        activities_inputs_data["scheme_class"] =scheme_class
        activities_inputs_data["scheme_sub_class"] =scheme_sub_class
        activities_inputs_data["funder"] = funder_id
        activities_inputs_data["transfer_class"] = transfer_class
        activities_inputs_data["sub_transfer_class"]= transfer_sub_class
        activities_inputs_data["implementer"]= implementer_id
        activities_inputs_data["double_count"]= double_counted
        activities_inputs_data["budget"] = 0
        activities_inputs_data["budget_currency"] ='RWF'
        if expenditure and isinstance(expenditure, str):
                print(f'!!!!!!!! { expenditure} type: {type(expenditure)}')
                activities_inputs_data["expenses"] =clean_decimal_string(str(expenditure))
                activities_inputs_data["expenses_currency"] ='RWF'
                activities_inputs_data["status"] = Activities_Inputs.STATUS_EXPENSES_APPROVED
                print()
                activity_input_err, activity_input_msg, activity_input = Methods_Activities_Inputs.update(request, user, activities_inputs_data, None)
    
def read_hrtt_csv_format(request):
    user = Users.login_required(request)
    
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    
    if request.method == 'POST' and request.FILES.get('excel_file'):
        file_path = request.FILES['excel_file']
        
        if not file_path.name.endswith('.csv'):
            return JsonResponse({'error': True,'message': "The uploaded file should be an hrtt .csv file format."}) 
        try:
            df = pd.read_csv(file_path, encoding='utf-8',index_col=False,low_memory=False, na_values=['', '-','nan', 'N/A', 'NA','NaN'])
            df.columns = df.columns.str.strip()
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            df.dropna(axis=0, how='all',inplace=True)  # Drop columns that are all NaN
            for _,row in df.iterrows():
                if not pd.isnull(row).all():
                    json_row = dict(row)
                    organization_name = json_row.get("Organization")
                    organization_type_code = json_row.get("Organization type code")
                    double_count = json_row.get("Double count (Y/N)")
                    project_name = json_row.get("Project")
                    funder_name = json_row.get("Funding Source")
                    fa_code = json_row.get("Financing agent class code")
                    fa_sub_code = json_row.get("Financing agent Sub-class code")
                    implementer_name =json_row.get("Implementer name")
                    activity_name = json_row.get("Activity")
                    location_name = json_row.get("Location name")
                    domain_code = json_row.get("Domain of intervention code")
                    sub_domain_code = json_row.get("Sub domain of intervetion code ")
                    function_name = json_row.get("Level 2 Sub domain")
                    care_provider_class = json_row.get("Health care provider class code")
                    care_provider_sub_class=json_row.get("Health care provider sub class code")
                    input_code =json_row.get("Input code")
                    input_sub_code = json_row.get("Input sub-class code")
                    fsc_fs_code = json_row.get(" Financing schemes and sources class Code")
                    fsc_fs_sub_code = json_row.get("Financing schemes and sources  sub class code")
                    expenditure = json_row.get("FRW Expenditure Amount ")
                    fiscal_year = json_row.get("FY")
                    
                    save_data(request, user,  
                    organization_name,
                    organization_type_code,
                    double_count,
                    project_name,
                    funder_name,
                    fa_code,
                    fa_sub_code,
                    implementer_name,
                    activity_name,
                    location_name,
                    domain_code,
                    sub_domain_code,
                    function_name,
                    care_provider_class,
                    care_provider_sub_class,
                    input_code,
                    input_sub_code,
                    fsc_fs_code,
                    fsc_fs_sub_code,
                    expenditure,
                    fiscal_year)
                
            messages.success(request, "Data uploaded successfully.")                   
            return JsonResponse({'message': 'success'}) 
        
        except Exception as e:
            return  JsonResponse({'error': True,'message': f"Error processing the CSV file: {str(e)}"}) 

    else:
        return  JsonResponse({'error': True,'message': "No file was uploaded."}) 
                
def read_rra_csv_format(request):
    template_url = "settings/index.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    
    if request.method == 'POST' and request.FILES.get('rra_file'):
        file_path = request.FILES['rra_file']
        
        if not file_path.name.endswith('.csv'):
            return JsonResponse({'error': True,'message': "The uploaded file should rra.csv file format."}) 
        try:    
            df = pd.read_csv(file_path, encoding='utf-8',index_col=False,low_memory=False, na_values=['', '-','nan', 'N/A', 'NA','NaN'])
            df.columns = df.columns.str.strip()
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            df.dropna(axis=0, how='all',inplace=True) 
        
            for _,row in df.iterrows():
                if not pd.isnull(row).all():
                    json_row = dict(row)
                    organization_name = json_row.get("Tax Payer Name"," ")
                    organization_type_code = "12"
                    double_count = "No"
                    project_name = "Own Revenues"
                    funder_name = "Health insurances and co-payment"
                    fa_code = "FA.3"
                    fa_sub_code = "FA.3.1"
                    implementer_name ="Pharmacies - Private"
                    activity_name = json_row.get("ISIC desc")
                    location_name = "Decentralized level/districts"
                    domain_code = "D.9"
                    sub_domain_code = "D.9.17"
                    function_name = "Medical goods (non-specified by function)"
                    care_provider_class = "HP.5"
                    care_provider_sub_class="HP.5.1"
                    input_code ="FP.3.4"
                    input_sub_code = "FP.3.4.3"
                    fsc_fs_code = "FS.6"
                    fsc_fs_sub_code = "FS.6.1"
                    expenditure = json_row.get("Business Income"," ")
                    fiscal_year = json_row.get("Fiscal Year"," ")
                    
                    save_data(request, user,  
                    organization_name,
                    organization_type_code,
                    double_count,
                    project_name,
                    funder_name,
                    fa_code,
                    fa_sub_code,
                    implementer_name,
                    activity_name,
                    location_name,
                    domain_code,
                    sub_domain_code,
                    function_name,
                    care_provider_class,
                    care_provider_sub_class,
                    input_code,
                    input_sub_code,
                    fsc_fs_code,
                    fsc_fs_sub_code,
                    expenditure,
                    fiscal_year)
                    
            messages.success(request, "Data uploaded successfully.")                   
            return JsonResponse({'message': 'success'})
        except Exception as e:
            return  JsonResponse({'error': True,'message': f"Error processing the CSV file: {str(e)}"}) 

    else:
        return  JsonResponse({'error': True,'message': "No file was uploaded."})  


def download_excel_view(request):
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
    return JsonResponse(data, safe=False)




def read_ifmis_json_file(request):
    template_url = "settings/index.html"
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if request.method == 'POST':
        if 'json_file' in request.FILES:
            json_file = request.FILES['json_file']

            # Check if the file has a .json extension
            if json_file.name.endswith('.json'):
                try:
                    # Read the contents of the JSON file
                    json_data = json_file.read().decode('utf-8')
                    # Parse the JSON data
                    data = json.loads(json_data)
                    # Do something with the data
                    data = json.dumps(data,indent=4, default=str)
                    data = json.loads(data)
                    for json_data in data:
                        organization_name = json_data.get("entityName", " ")
                        organization_type_code = " "
                        double_count = "No"
                        project_name = json_data.get("fundingTypeName"," ")
                        funder_name = " "
                        fa_code = " "
                        fa_sub_code = " "
                        implementer_name = " "
                        activity_name = json_data.get("activityName"," ")
                        location_name = json_data.get("districtName"," ")
                        domain_name = json_data.get("programName"," ")
                        sub_domain_name = json_data.get("subProgramName"," ")
                        function_name = " " 
                        care_provider_class = " "
                        care_provider_sub_class = " "
                        input_code_to_map = json_data.get("ecoItemCode"," ")
                        capital_code = json_data.get("ecoItemCode"," ")
                        scheme_name = json_data.get("fundingSourceName"," ")
                        sub_scheme_name = json_data.get("fundingTypeName"," ")
                        fiscal_year = json_data.get("fiscalYear"," ")
                        budget_amaount = json_data.get('budgetAmount','0.0')
                        remained_budget = json_data.get('budgetBalance','0.0')
                        
                        ecoClass = json_data.get("ecoClassCode",0)
                                  
                        if domain_name and isinstance(domain_name,str):
                            try:
                                domain = Levels.objects.get(Q(level_name = domain_name) & Q(level_key='domain') )
                                domain_code = domain.level_code
                            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                                domain_code = " "
                                
                        if sub_domain_name and isinstance(sub_domain_name, str):
                            try:
                                sub_domain = Levels.objects.get(Q(level_name = sub_domain_name ) & Q(level_key ='sub-domain') )
                                sub_domain_code = sub_domain.level_code
                            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                                sub_domain_code = " "
                                
                        if input_code_to_map and isinstance(input_code_to_map,str):
                            try:
                                sub_input = hrtt_inputs_factory.get(input_code_to_map)
                                input_level = Levels.objects.get(Q(level_id = sub_input.level_parent) & Q(level_key ='inputs') )
                                input_sub_code = sub_input.level_code
                                input_code = input_level.level_code
                            except:
                                input_sub_code = " "
                                input_code = " "
                                
                        if scheme_name and isinstance(scheme_name,str):
                            try:
                                scheme_class = Levels.objects.get(Q(level_name = scheme_name) & Q(level_key ='financing-scheme-type') )
                                fsc_fs_code = scheme_class.level_code
                            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                                fsc_fs_code = " "
                        if sub_scheme_name and isinstance(sub_scheme_name,str):
                            try:
                                scheme_sub_class = Levels.objects.get(Q(level_name = sub_scheme_name) & Q(level_key ='financing-scheme-type'))
                                fsc_fs_sub_code = scheme_sub_class.level_code
                            except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
                                fsc_fs_sub_code = " "
                                
                        if budget_amaount and remained_budget:
                            expenditure = float(budget_amaount) - float(remained_budget)
                            
                        if fiscal_year and isinstance(fiscal_year,str):
                            fiscal_year = fiscal_year.replace("/", "-")
                            
                        if int(ecoClass) == 2 :
                            
                            save_data(request, user,  
                                organization_name,
                                organization_type_code,
                                double_count,
                                project_name,
                                funder_name,
                                fa_code,
                                fa_sub_code,
                                implementer_name,
                                activity_name,
                                location_name,
                                domain_code,
                                sub_domain_code,
                                function_name,
                                care_provider_class,
                                care_provider_sub_class,
                                input_code,
                                input_sub_code,
                                fsc_fs_code,
                                fsc_fs_sub_code,
                                expenditure,
                                fiscal_year)
                            
                        if int(ecoClass) == 3 :
                            # handle capital saving
                            pass
                    return redirect(reverse("users_dashboard"))
                except json.JSONDecodeError:
                    
                    msg = "Invalid JSON content in the file."
                    messages.error(request, msg)
                    return render(
                        request,
                        template_url,
                        {
                            "section": settings.BACKEND_SECTION_SETTINGS,
                            "title": "Settings",
                            "name": "settings",
                            "user": user,
                            "auth_permissions": auth_permissions,
                            "fiscal_year_choices":fiscal_year_choices,
                        },
                    )
            else:
                msg = "The uploaded file should be a JSON file."
                messages.error(request, msg)
                return render(
                        request,
                        template_url,
                        {
                            "section": settings.BACKEND_SECTION_SETTINGS,
                            "title": "Settings",
                            "name": "settings",
                            "user": user,
                            "auth_permissions": auth_permissions,
                            "fiscal_year_choices":fiscal_year_choices,
                        },
                    )
        else:
            msg = "No file was uploaded."
            messages.error(request, msg)
            return render(
            request,
            template_url,
            {
                "section": settings.BACKEND_SECTION_SETTINGS,
                "title": "Settings",
                "name": "settings",
                "user": user,
                "auth_permissions": auth_permissions,
                "fiscal_year_choices":fiscal_year_choices,
            },
        )

    return HttpResponseBadRequest("Invalid request method.")
    


