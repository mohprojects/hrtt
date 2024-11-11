import asyncio
import json

from app import settings
from app.data import ARRAY_KIGALI_AREAS, ARRAY_RWANDA_DISTRICTS
from app.models.access_permissions import Access_Permissions
from app.models.failed_login import Failed_Login
from app.models.methods.access_permissions import Methods_Access_Permissions
from app.models.methods.emails import Methods_Emails
from app.models.methods.failed_login import Methods_Failed_Login
from app.models.methods.logs import Methods_Logs
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.user_access_permissions import \
    Methods_User_Access_Permissions
from app.models.methods.users import Methods_Users
from app.models.user_access_permissions import User_Access_Permissions
from app.models.users import Users
from app.models.organizations import Organizations
from app.models.methods.organizations import Methods_Organizations
from app.models.projects import Projects
from app.models.activities import Activities
from app.models.activities_inputs import Activities_Inputs
from app.utils import Utils
from backend.forms.user_forms import (UserChangePasswordForm,
                                          UserCreateForm,
                                          UserForgotPasswordForm,
                                          UserProfileUpdateForm,
                                          UserResetPasswordForm,
                                          UserSearchIndexForm,
                                          UserSignInCaptchaForm,
                                          UserSignInForm,
                                          UserUpdateForm, UserViewForm)
from backend.tables.logs_tables_view import LogsTableView
from backend.tables.user_tables import UsersTable
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound)
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View



def confirm(request, token):
    try:
        user = Users.objects.get(user_auth_key=token)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None
    if user is None:
        messages.info(request, 'Invalid token.')
        return redirect(reverse("users_signin"))
    model = user
    Methods_Users.update_status(
        request, user, model, Users.STATUS_INACTIVE)
    messages.info(
        request, 'Thank you for your email confirmation. You will be able to login After the Admin approved your account.')
    return redirect(reverse("users_signin"))


def signin(request):
    template_url = 'users/signin.html'
    failed_count = Failed_Login.objects.filter(failed_login_from=Failed_Login.FAILED_LOGIN_FROM_BACKEND,
                                               failed_login_ip_address=Utils.get_ip_address(
                                                   request),
                                               failed_login_status=False).count()
    display_captcha = False
    # if failed_count >= settings.MAX_LOGIN_ATTEMPTS_CAPTCHA:
    #     display_captcha = True
    if request.method == 'POST':
        if display_captcha:
            form = UserSignInCaptchaForm(request.POST)
        else:
            form = UserSignInForm(request.POST)
        if form.is_valid():
            try:
                user = Users.objects.get(
                    user_username=form.cleaned_data['email'])
            except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
                user = None
            if user is None:
                Methods_Failed_Login.add(form.cleaned_data['email'], form.cleaned_data['password'],
                                         Failed_Login.FAILED_LOGIN_FROM_BACKEND,
                                         Utils.get_ip_address(request), False)
                messages.error(
                    request, 'Incorrect email address or password.')
                return render(request, template_url, {'form': form, 'display_captcha': display_captcha})
            else:
                model = user
                #organization = Organizations.objects.get(organization_id = model.organization_id)
                try:
                    organization = Organizations.objects.get(organization_id = model.organization_id)
                    organization_name =organization.organization_name
                except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                   organization_name=""

                if model.user_status == Users.STATUS_UNVERIFIED:
                    model.user_password_reset_token = Users.generate_unique_token(Users,'user_password_reset_token')
                    model.save()
                    action_url = '{domain}/{path}'.format(
                        domain=Utils.get_backend_domain(),
                        path='users/reset-password/' + model.user_password_reset_token
                    )
                    Methods_Emails.send_verification_email(
                        request, model.user_username, model.user_name,model.user_role,organization_name,action_url)
                    messages.error(
                        request, 'Your email address is not yet verified. Please check your mail to confirm.')
                    return render(request, template_url, {'form': form, 'display_captcha': display_captcha})
                # elif model.user_status == Users.STATUS_UNAPPROVED:
                #     messages.error(
                #         request, 'Your account is not yet approved. Please contact admin for support.')
                #     return render(request, template_url, {'form': form, 'display_captcha': display_captcha})
                elif model.user_status == Users.STATUS_BLOCKED:
                    messages.error(
                        request, 'Your account is blocked. Please contact admin for support.')
                    return render(request, template_url, {'form': form, 'display_captcha': display_captcha})
                elif check_password(form.cleaned_data['password'], make_password(Users.DEFAULT_PASSWORD)):
                    messages.error(
                        request, 'Default Password Should be Reset First')
                    return render(request, template_url, {'form': form, 'display_captcha': display_captcha})

                elif check_password(form.cleaned_data['password'], model.user_password_hash):
                    try:
                        organization = Organizations.objects.get(organization_id = model.organization_id)
                        if organization.organization_status == Organizations.STATUS_INNACTIVE:
                            Methods_Organizations.update_status( request, user, organization, Organizations.STATUS_ACTIVE)
                    except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                        pass
                    
                    Methods_Users.update_status(
                        request, user, model, Users.STATUS_ACTIVE)
                    Users.login(request, model)
                    Failed_Login.objects.filter(failed_login_from=Failed_Login.FAILED_LOGIN_FROM_BACKEND,
                                                failed_login_ip_address=Utils.get_ip_address(
                                                    request),
                                                failed_login_status=False).update(failed_login_status=True)
                    redirect_field_name = Users.get_redirect_field_name(
                        request)
                    
                    asyncio.run(
                        Methods_Logs.add(
                            settings.MODEL_USERS, 
                            model.user_id, 
                            'User login.', 
                            model.user_id, 
                            model.user_name
                        )
                    )
                    
                    model.save()

                    return redirect(reverse("users_dashboard"))
                    # if redirect_field_name is None:
                    #     return redirect(reverse("users_dashboard"))
                    # else:
                    #     return redirect(redirect_field_name)
                else:
                    Methods_Failed_Login.add(form.cleaned_data['email'], form.cleaned_data['password'],
                                             Failed_Login.FAILED_LOGIN_FROM_BACKEND,
                                             Utils.get_ip_address(request), False)
                    messages.error(
                        request, 'Incorrect email address or password.')
                    return render(request, template_url, {'form': form, 'display_captcha': display_captcha})
        else:
            messages.error(request, form.errors.as_data())
            return render(request, template_url, {'form': form, 'display_captcha': display_captcha})

    if display_captcha:
        form = UserSignInCaptchaForm()
    else:
        form = UserSignInForm()
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    return render(request, template_url, {'form': form, 'display_captcha': display_captcha})


def forgot_password(request):
    template_url = 'users/forgot-password.html'
    if request.method == 'POST':
        form = UserForgotPasswordForm(request.POST)
        if form.is_valid():
            try:
                user = Users.objects.get(
                    user_username=form.cleaned_data['email'])
            except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
                user = None
            if user is None:
                messages.error(
                    request, 'Email Id: "%s" is not yet registered.' % form.cleaned_data['email'])
                return render(request, template_url,
                              {'form': form})
            else:
                model = user
                try:
                    organization = Organizations.objects.get(organization_id = model.organization_id)
                    organization_name =organization.organization_name
                except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                    organization_name=""
                if model.user_status == Users.STATUS_UNVERIFIED:
                  
                    model.user_password_reset_token = Users.generate_unique_token(Users,'user_password_reset_token')
                    model.save()
                    action_url = '{domain}/{path}'.format(
                        domain=Utils.get_backend_domain(),
                        path='users/reset-password/' + model.user_password_reset_token
                    )
                    Methods_Emails.send_verification_email(
                        request, model.user_username, model.user_name,model.user_role,organization_name,action_url)
                    messages.error(request,
                                   'Your email address is not yet verified. Please check your mail to confirm.')
                    return render(request, template_url,
                                  {'form': form})
         
                elif model.user_status == Users.STATUS_BLOCKED:
                    messages.error(
                        request, 'Your account is blocked. Please contact admin for support.')
                    return render(request, template_url,
                                  {'form': form})
                else:
                    model.user_password_reset_token = Users.generate_unique_token(Users,'user_password_reset_token')
                    model.save()
                    action_url = '{domain}/{path}'.format(
                        domain=Utils.get_backend_domain(),
                        path='users/reset-password/' + model.user_password_reset_token
                    )
                    Methods_Emails.send_reset_password_email(
                        request, model.user_username, model.user_name, action_url)
                    messages.info(
                        request, 'An email has been sent to reset your password.')
                    
                    asyncio.run(
                        Methods_Logs.add(
                            settings.MODEL_USERS, 
                            model.user_id, 
                            'User forgot password.', 
                            model.user_id, 
                            model.user_name
                        )
                    )
                    return redirect(reverse("users_signin"))
        else:
            form = UserForgotPasswordForm()
            return render(request, template_url, {'form': form})
    form = UserForgotPasswordForm()
    return render(request, template_url, {'form': form})


def reset_password(request, token):
    template_url = 'users/reset-password.html'
    try:
        user = Users.objects.get(user_password_reset_token=token)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None
    if user is None:
        return redirect(reverse("users_signin"))
    model = user

    if request.method == 'POST':
        form = UserResetPasswordForm(request.POST)
        form.fields["email"].initial = model.user_username
        if form.is_valid():
            model.user_password_hash = make_password(
                form.cleaned_data['password'])
            model.user_password_reset_token = ''
            model.save()
            if model.user_status == Users.STATUS_UNVERIFIED:
                Methods_Users.update_status(request, user, model, Users.STATUS_INACTIVE)
            messages.info(
                request, 'Your password has been reset successfully.')
            asyncio.run(
                        Methods_Logs.add(
                            settings.MODEL_USERS, 
                            model.user_id, 
                            'User reset password.', 
                            model.user_id, 
                            model.user_name
                        )
                    )
            return redirect(reverse("users_signin"))
        else:
            form.fields["email"].initial = model.user_username
            return render(request, template_url, {'form': form})

    form = UserResetPasswordForm()
    form.fields["email"].initial = model.user_username
    return render(request, template_url, {'form': form})


def signout(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    model = user
    Methods_Users.update_status(
        request, user, model, Users.STATUS_INACTIVE)
    # logout
    Users.logout(request)

    model.save()

    return redirect(reverse("users_signin"))


def dashboard(request):
    template_url = 'users/dashboard.html'
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)

    midnight = Utils.get_midnight_datetime_utc()
    current_year = Utils.get_current_year()
    prev_year = int(current_year) -1
    fiscal_year = f"{prev_year}-{current_year}"
    fiscal_year_choices = Utils.get_fiscal_year_choices_for_system_report()
    
    users_objects = Users.objects.all()
    users_activity_manager= users_objects.filter(user_role = Users.TYPE_ACTIVITY_MANAGER)
    users_data_reporters = users_objects.filter(user_role = Users.TYPE_DATA_REPORTER) 
    other_users = users_objects.exclude(Q(user_role = Users.TYPE_ACTIVITY_MANAGER))
    other_users = other_users.exclude(Q(user_role = Users.TYPE_DATA_REPORTER))
    organizations_objects = Organizations.objects.all()
    projects_objects = Projects.objects.all()
    activities_objects = Activities.objects.all()
    # users
    count_users = users_objects.count()
    count_users_activity_manager = users_activity_manager.count()
    count_users_data_reporters = users_data_reporters.count()
    count_other_users = other_users.count()
    count_organizations = organizations_objects.count()
    # count_divisions  = divisions_objects.count()
    count_projects = projects_objects.count()
    count_activities = activities_objects.count()

    # activity manager
    if user.user_role == Users.TYPE_ACTIVITY_MANAGER:
        users_objects = users_objects.filter(Q(user_created_by = user.user_id))
        users_data_reporters = users_objects.filter(user_role = Users.TYPE_DATA_REPORTER)
        other_users = users_objects.exclude(Q(user_role = Users.TYPE_ACTIVITY_MANAGER))
        other_users = other_users.exclude(Q(user_role = Users.TYPE_DATA_REPORTER)) 
        projects_objects = Projects.objects.filter(Q(organization_id = user.organization_id))
        filter_project_ids = projects_objects.values_list('project_id', flat=True)
        activities_objects = Activities.objects.filter(Q(project_id__in = filter_project_ids)) 
        count_users_data_reporters = users_data_reporters.count()
        count_users = users_objects.count()
        count_other_users = other_users.count()
        count_organizations = organizations_objects.filter(Q(organization_id = user.organization_id)).count()
        count_projects = projects_objects.count()
        count_activities = activities_objects.count()

    if user.user_role == Users.TYPE_DATA_REPORTER:
        projects_objects = Projects.objects.filter(Q(organization_id = user.organization_id) & Q(project_assigned_to = user.user_id))
        filter_project_ids = projects_objects.values_list('project_id', flat=True)
        activities_objects = Activities.objects.filter(Q(project_id__in = filter_project_ids)) 
        count_projects = projects_objects.count()
        count_activities = activities_objects.count()

    reported_activities_budget= Activities.objects.filter(Q(activity_status = Activities.STATUS_BUDGET_APPROVED) & Q(activity_fiscal_year = fiscal_year))
    reported_activities_expenditure= Activities.objects.filter(Q(activity_status = Activities.STATUS_EXPENSES_APPROVED) & Q(activity_fiscal_year = fiscal_year))

    filtered_organization_budget_ids = reported_activities_budget.values_list('organization_id', flat=True).distinct()
    filtered_organization_expenditure_ids =reported_activities_expenditure.values_list('organization_id', flat=True).distinct()
  
    count_reported_organizations_budget= len(filtered_organization_budget_ids) + len(filtered_organization_expenditure_ids)
    count_reported_organizations_expenditure= len(filtered_organization_expenditure_ids)

    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_DASHBOARD,
            'title': 'Dashboard',
            'name': 'dashboard',
            'user': user,
            'auth_permissions': auth_permissions,
            'count_users': count_users,
            'count_users_activity_manager':count_users_activity_manager,
            'count_users_data_reporters':count_users_data_reporters,
            'count_other_users':count_other_users,
            'count_organizations':count_organizations,
            'count_reported_organizations_budget': count_reported_organizations_budget,
            'count_reported_organizations_expenditure':count_reported_organizations_expenditure,
            'count_projects':count_projects,
            'count_activities':count_activities,
            'current_year':current_year,
            'fiscal_year_choices':fiscal_year_choices

        }
    )

class AjaxUsersList(View):
    def get(self, request):
        user = Users.login_required(request)
        if user is None:
            return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type='application/json')
        items = self._datatables(request, user)
        return HttpResponse(json.dumps(items, cls=DjangoJSONEncoder), content_type='application/json')

    def _datatables(self, request, user: Users):
        auth_permissions = Methods_Users.get_auth_permissions(user)

        column1 = 'user_username'
        column2 = 'user_name'
        column3 = 'user_contact_phone_number'
        column4 = 'organization_id'
        column5 = 'user_role'
        column6 = 'user_status'

        datatables = request.GET

        # item draw
        draw = int(datatables.get('draw'))
        # item start
        start = int(datatables.get('start'))
        # item length (limit)
        length = int(datatables.get('length'))
        # item data search
        search = datatables.get('search[value]')

        # Get objects
        objects = Users.objects
        if user.user_role == Users.TYPE_ACTIVITY_MANAGER:
            objects = Users.objects.filter(Q(organization_id = user.organization_id) & Q(user_role = Users.TYPE_DATA_REPORTER))

        # Set record total
        records_total = objects.all().count()
        # Set records filtered
        records_filtered = records_total

        order_column_index = datatables.get('order[0][column]')
        order_column_sort = datatables.get('order[0][dir]')

        if order_column_index and order_column_sort:
            if int(order_column_index) == 1:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column1)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column1)
            if int(order_column_index) == 2:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column2)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column2)
            if int(order_column_index) == 3:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column3)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column3)
            if int(order_column_index) == 4:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column4)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column4)
            if int(order_column_index) == 5:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column5)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column5)
            if int(order_column_index) == 6:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column6)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column6)

        objects_filter = False
        if search:
            objects_filter = True
            if search == '-':
                filter_organizations = [0]
            else:
                filter_organizations = Organizations.objects.filter(
                    Q(organization_name__icontains=search)
                )
        
            objects = objects.filter(
                Q(user_username__icontains=search) |
                Q(user_name__icontains=search) |
                Q(user_contact_phone_number__icontains=search) |
                Q(organization_id__in=filter_organizations) |
                Q(user_role__icontains=search)
            )

        column_index = 1
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(user_username__icontains=column_search)
            )

        column_index = 2
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(user_name__icontains=column_search)
            )

        column_index = 3
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(user_contact_phone_number__icontains=column_search)
            )
        
        column_index = 4
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
       
        if column_search != '':
            objects_filter = True
            if column_search == '-':
                filter_organizations = [0]
            else:
                
                filter_organizations = Organizations.objects.filter(
                    Q(organization_name__icontains=column_search)
                )
            objects = objects.filter(
                Q(organization_id__in=filter_organizations)
            )
        
        column_index = 5
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            role_search =column_search.lower().replace(' ', '-') 
            objects_filter = True
            objects = objects.filter(
                Q(user_role__icontains=role_search)
            )

        column_index = 6
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(user_status=Users.ARRAY_TEXT_STATUS.index(column_search))
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
            row_number = UsersTable.render_row_number(record, counter)
            value1 = UsersTable.render_user_username(record)
            value2 = UsersTable.render_user_name(record)
            value3 = UsersTable.render_user_contact_phone_number(record)
            value4 = UsersTable.render_organization_id(record)
            # value5 = UsersTable.render_division_id(record)
            value6 = UsersTable.render_user_role(record)
            value7 = UsersTable.render_user_status(record)
            actions = UsersTable.render_actions(record, auth_permissions)

            data.append({
                'row_number': row_number,
                'user_username': value1,
                'user_name': value2,
                'user_contact_phone_number': value3,
                'organization_id': value4,
                # 'division_id': value5,
                'user_role': value6,
                'user_status': value7,
                'actions': actions,
            })

        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


def json_users(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    return HttpResponse(serializers.serialize("json", Users.objects.all()),
                        content_type="application/json")


def index(request):
    template_url = 'users/index.html'
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')

    search_form = UserSearchIndexForm(request.POST or None)
    if request.method == 'POST' and search_form.is_valid():
        display_search = True
    else:
        display_search = False

    objects = {}
    table = UsersTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_USERS,
            'title': Users.TITLE,
            'name': Users.NAME,
            'user': user,
            'auth_permissions': auth_permissions,
            'table': table,
            'search_form': search_form,
            'display_search': display_search,
            'index_url': reverse("users_index"),
            'select_multiple_url': reverse("users_select_multiple"),
        }
    )


@csrf_exempt
def select_single(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse('signin', content_type='text/plain')
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    action = request.POST['action']
    id = request.POST['id']
    if action == '' or id is None:
        return HttpResponseBadRequest('Bad Request', content_type='text/plain')
    try:
        model = Users.objects.get(pk=id)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        return HttpResponseBadRequest('Bad Request', content_type='text/plain')

    if action == 'verify':
        if model.user_status == Users.STATUS_UNVERIFIED:
            Methods_Users.update_status(
                request, user, model, Users.STATUS_INACTIVE)
            messages.success(request, 'Verified successfully.')

    if action == 'block':
        if model.user_status == Users.STATUS_ACTIVE or model.user_status == Users.STATUS_INACTIVE:
            Methods_Users.update_status(
                request, user, model, Users.STATUS_BLOCKED)
            messages.success(
                request, 'Blocked successfully.')

    if action == 'unblock':
        if model.user_status == Users.STATUS_BLOCKED:
            Methods_Users.update_status(
                request, user, model, Users.STATUS_INACTIVE)
            messages.success(
                request, 'Unblocked successfully.')

    if action == 'delete':
        if settings.ACCESS_PERMISSION_USER_DELETE not in auth_permissions.values():
            return HttpResponseForbidden('Forbidden', content_type='text/plain')
        Methods_Users.delete(request, user, model)
        messages.success(request, 'Deleted successfully.')
    
    return HttpResponse('success', content_type='text/plain')


@csrf_exempt
def select_multiple(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse('signin', content_type='text/plain')
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    action = request.POST['action']
    ids = request.POST['ids']
    try:
        ids = ids.split(",")
    except(TypeError, ValueError, OverflowError):
        ids = None
    if action == '' or ids is None:
        return HttpResponseBadRequest('Bad Request', content_type='text/plain')

    if action == 'verify':
        for id in ids:
            try:
                model = Users.objects.get(pk=id)
                if model.user_status == Users.STATUS_UNVERIFIED:
                    Methods_Users.update_status(
                        request, user, model, Users.STATUS_INACTIVE)
            except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
                continue
        messages.success(request, 'Verified successfully.')

    # if action == 'approve':
    #     for id in ids:
    #         try:
    #             model = Users.objects.get(pk=id)
    #             if model.user_status == Users.STATUS_UNAPPROVED:
    #                 Methods_Users.update_status(
    #                     request, user, model, Users.STATUS_INACTIVE)
    #         except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
    #             continue
    #     messages.success(request, 'Approved successfully.')

    if action == 'block':
        for id in ids:
            try:
                model = Users.objects.get(pk=id)
                if model.user_status == Users.STATUS_ACTIVE or model.user_status == Users.STATUS_INACTIVE:
                    Methods_Users.update_status(
                        request, user, model, Users.STATUS_BLOCKED)
            except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
                continue
        messages.success(request, 'Blocked successfully.')

    if action == 'unblock':
        for id in ids:
            try:
                model = Users.objects.get(pk=id)
                if model.user_status == Users.STATUS_BLOCKED:
                    Methods_Users.update_status(
                        request, user, model, Users.STATUS_INACTIVE)
            except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
                continue
        messages.success(request, 'Unblocked successfully.')

    if action == 'delete':
        if settings.ACCESS_PERMISSION_USER_DELETE not in auth_permissions.values():
            return HttpResponseForbidden('Forbidden', content_type='text/plain')
        for id in ids:
            try:
                model = Users.objects.get(pk=id)
                Methods_Users.delete(request, user, model)
            except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
                continue
        messages.success(request, 'Deleted successfully.')

    return HttpResponse('success', content_type='text/plain')


def create(request):
    template_url = 'users/create.html'
    permissions_list = None
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_CREATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')

    if request.method == 'POST':
        form = UserCreateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "email": form.cleaned_data['email'],
                "password": Users.DEFAULT_PASSWORD,
                #"name": form.cleaned_data['name'],
                "first_name": form.cleaned_data["first_name"],
                "middle_name": form.cleaned_data["middle_name"],
                "last_name": form.cleaned_data["last_name"],
                "phone_number": form.cleaned_data['phone_number'],
                "organization_id": form.cleaned_data['organization_id'],
                #"division_id": form.cleaned_data['division_id'],
                "role": form.cleaned_data['role'],
            }
            err, msg, model = Methods_Users.create(request, user, data)
            if err:
                messages.error(request, msg)
                return render(
                    request, template_url,
                    {
                        'section': settings.BACKEND_SECTION_USERS,
                        'title': Users.TITLE,
                        'name': Users.NAME,
                        'user': user,
                        'auth_permissions': auth_permissions,
                        'form': form,
                    }
                )
            if model.user_role == Users.TYPE_SUPER_ADMIN:
                permissions_list = Users.ADMIN_DEFAULT_PERMISSIONS_LIST
            if model.user_role == Users.TYPE_ACTIVITY_MANAGER:
                permissions_list = Users.ACTIVITY_MANAGER_DEFAULT_PERMISSIONS_LIST
            if model.user_role == Users.TYPE_DATA_REPORTER:
                permissions_list = Users.DATA_REPORTERS_DEFAULT_PERMISSIONS_LIST
            if permissions_list is not None:
                i = 0
                while i < len(permissions_list):
                    if permissions_list[i]:
                        access_permission = Access_Permissions.objects.get(
                            access_permission_name=permissions_list[i])
                        user_access_permission = User_Access_Permissions()
                        user_access_permission.access_permissions_access_permission_name = access_permission
                        user_access_permission.users_user_id = model
                        user_access_permission.user_access_permission_updated_at = Utils.get_current_datetime_utc()
                        user_access_permission.user_access_permission_updated_by = user.user_id
                        user_access_permission.save()
                    i += 1

            # action_url = '{domain}/{path}'.format(
            #     domain=Utils.get_backend_domain(),
            #     path='users/signup/confirm/' + model.user_auth_key
            # )
            model.user_password_reset_token = Users.generate_unique_token(Users,'user_password_reset_token')
            model.save()
            try:
                organization = Organizations.objects.get(organization_id = model.organization_id)
                organization_name =organization.organization_name
            except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                organization_name=""
            action_url = '{domain}/{path}'.format(
                        domain=Utils.get_backend_domain(),
                        path='users/reset-password/' + model.user_password_reset_token
                    )
            Methods_Emails.send_verification_email(
                request, model.user_username, model.user_name,model.user_role,organization_name, action_url)
            messages.info(
                request, 'An email has been sent for verification to the registered email address.')
            asyncio.run(
                        Methods_Logs.add(
                            settings.MODEL_USERS, 
                            model.user_id, 
                            'Created user.', 
                            user.user_id, 
                            user.user_name
                        )
                    )
            return redirect(reverse("users_view", args=[model.user_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_USERS,
                    'title': Users.TITLE,
                    'name': Users.NAME,
                    'user': user,
                    'auth_permissions': auth_permissions,
                    'form': form,
                }
            )

    form = UserCreateForm(user=user)
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_USERS,
            'title': Users.TITLE,
            'name': Users.NAME,
            'user': user,
            'auth_permissions': auth_permissions,
            'form': form,
        }
    )


def update(request, pk):
    template_url = 'users/update.html'
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Users.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, user=user)
        if form.is_valid():
            data = {
                "email": form.cleaned_data['email'],
                #"name": form.cleaned_data['name'],
                "first_name": form.cleaned_data["first_name"],
                "middle_name": form.cleaned_data["middle_name"],
                "last_name": form.cleaned_data["last_name"],
                "phone_number": form.cleaned_data['phone_number'],
                "organization_id": form.cleaned_data['organization_id'],
               # "division_id": form.cleaned_data['division_id'],
                "role": form.cleaned_data['role'],
            }
            err, msg, model = Methods_Users.update(request, user, data, model)
            if err:
                messages.error(request, msg)
                return render(
                    request, template_url,
                    {
                        'section': settings.BACKEND_SECTION_USERS,
                        'title': Users.TITLE,
                        'name': Users.NAME,
                        'user': user,
                        'auth_permissions': auth_permissions,
                        'form': form,
                        'model': model,
                    }
                )
            messages.success(request, 'Updated successfully.')
            asyncio.run(
                        Methods_Logs.add(
                            settings.MODEL_USERS, 
                            model.user_id, 
                            'Updated user.', 
                            user.user_id, 
                            user.user_name
                        )
                    )
            return redirect(reverse("users_view", args=[model.user_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_USERS,
                    'title': Users.TITLE,
                    'name': Users.NAME,
                    'user': user,
                    'auth_permissions': auth_permissions,
                    'form': form,
                    'model': model,
                }
            )

    form = UserUpdateForm(
        user=user,
        initial=Methods_Users.form_view(request, user, model)
    )
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_USERS,
            'title': Users.TITLE,
            'name': Users.NAME,
            'user': user,
            'auth_permissions': auth_permissions,
            'form': form,
            'model': model,
        }
    )


def update_permissions_view(request, pk):
    template_url = 'users/update-permissions.html'
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Users.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, user=user)
        if form.is_valid():
            model.save()
            messages.success(
                request, 'Updated permissions successfully.')
            asyncio.run(
                        Methods_Logs.add(
                            settings.MODEL_USERS, 
                            model.user_id, 
                            'Updated user permissions.', 
                            user.user_id, 
                            user.user_name
                        )
                    )
            return redirect(reverse("users_view", args=[model.user_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_USERS,
                    'title': Users.TITLE,
                    'name': Users.NAME,
                    'user': user,
                    'auth_permissions': auth_permissions,
                    'form': form,
                    'model': model,
                }
            )

    form = UserUpdateForm(
        user=user,
        initial=Methods_Users.form_view(request, user, model)
    )
    auth= Methods_User_Access_Permissions.get_access_permissions(model.user_id)
    form.fields['email'].widget.attrs['readonly'] = 'true'
    form.fields['email'].widget.attrs['disabled'] = 'true'
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_USERS,
            'title': Users.TITLE,
            'name': Users.NAME,
            'user': user,
            'auth_permissions': auth_permissions,
            'form': form,
            'model': model,
            'all_auth_permissions': Methods_Access_Permissions.get_access_permissions(),
            'user_auth_permissions': Methods_User_Access_Permissions.get_access_permissions(
                model.user_id),
        }
    )


def update_permissions_action(request):
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    id = request.POST['id']
    permissions = request.POST['permissions']
    permissions_list = None
    if permissions != '' and permissions != 'null':
        permissions_list = permissions.split(",")
    try:
        model = Users.objects.get(pk=id)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    # delete existing permissions
    User_Access_Permissions.objects.filter(
        users_user_id=id).delete()
    if permissions_list is not None:
        i = 0
        while i < len(permissions_list):
            if permissions_list[i]:
                access_permission = Access_Permissions.objects.get(
                    access_permission_name=permissions_list[i])
                user_access_permission = User_Access_Permissions()
                user_access_permission.access_permissions_access_permission_name = access_permission
                user_access_permission.users_user_id = model
                user_access_permission.user_access_permission_updated_at = Utils.get_current_datetime_utc()
                user_access_permission.user_access_permission_updated_by = user.user_id
                user_access_permission.save()
            i += 1
    messages.success(request, 'Updated permissions successfully.')
    asyncio.run(
                        Methods_Logs.add(
                            settings.MODEL_USERS, 
                            model.user_id, 
                            'Updated user permissions.', 
                            user.user_id, 
                            user.user_name
                        )
                    )
    return HttpResponse('success', content_type='text/plain')


def update_reset_password(request, pk):
    template_url = 'users/update-reset-password.html'
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Users.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    if request.method == 'POST':
        form = UserResetPasswordForm(request.POST)
        form.fields["email"].initial = model.user_username
        if form.is_valid():
            model.user_password_hash = make_password(
                form.cleaned_data['password'])
            model.user_password_reset_token = ''
            model.save()
            Methods_Emails.send_info_email(
                request, model.user_username, model.user_name, 'Your password has been reset successfully by admin.')
            messages.info(request, 'Password has been reset successfully.')
            asyncio.run(
                        Methods_Logs.add(
                            settings.MODEL_USERS, 
                            model.user_id, 
                            'Reset user password.', 
                            user.user_id, 
                            user.user_name
                        )
                    )
            return redirect(reverse("users_view", args=[model.user_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_PROFILE,
                    'title': Users.TITLE,
                    'name': Users.NAME,
                    'user': user,
                    'auth_permissions': auth_permissions,
                    'form': form,
                    'model': model,
                }
            )
    form = UserResetPasswordForm()
    form.fields["email"].initial = model.user_username
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_PROFILE,
            'title': Users.TITLE,
            'name': Users.NAME,
            'user': user,
            'auth_permissions': auth_permissions,
            'form': form,
            'model': model,
        }
    )


def view(request, pk):
    template_url = 'users/view.html'
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Users.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    model = Methods_Users.format_view(request, user, model)
    form = UserViewForm(
        user=user,
        initial=Methods_Users.form_view(request, user, model)
    )
    count_logs = Methods_Mongo.get_collection(settings.MODEL_LOGS).count_documents({'model': 'users', 'modelId': model.user_id})

    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_USERS,
            'title': Users.TITLE,
            'name': Users.NAME,
            'user': user,
            'auth_permissions': auth_permissions,
            'model': model,
            'form': form,
            'index_url': reverse("users_index"),
            'select_single_url': reverse("users_select_single"),
            'count_logs': count_logs,
        }
    )


def profile_view(request):
    template_url = 'users/profile-view.html'
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    model = user
    model = Methods_Users.format_view(request, user, model)

    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_PROFILE,
            'title': Users.TITLE,
            'name': Users.NAME,
            'user': user,
            'auth_permissions': auth_permissions,
            'model': model,
        }
    )


def profile_update(request):
    template_url = 'users/profile-update.html'
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    model = user
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST)
        if form.is_valid():
            data = {
                "email": form.cleaned_data['email'],
                #"name": form.cleaned_data['name'],
                "first_name": form.cleaned_data["first_name"],
                "middle_name": form.cleaned_data["middle_name"],
                "last_name": form.cleaned_data["last_name"],
                "phone_number": form.cleaned_data['phone_number'],
            }
            err, msg, model = Methods_Users.update(request, user, data, model)
            if err:
                messages.error(request, msg)
                return render(
                    request, template_url,
                    {
                        'section': settings.BACKEND_SECTION_PROFILE,
                        'title': Users.TITLE,
                        'name': Users.NAME,
                        'user': user,
                        'auth_permissions': auth_permissions,
                        'form': form,
                    }
                )
            messages.success(request, 'Updated successfully.')
            asyncio.run(
                        Methods_Logs.add(
                            settings.MODEL_USERS, 
                            model.user_id, 
                            'User profile updated.', 
                            user.user_id, 
                            user.user_name
                        )
                    )
            return redirect(reverse("users_profile_view"))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_PROFILE,
                    'title': Users.TITLE,
                    'name': Users.NAME,
                    'user': user,
                    'auth_permissions': auth_permissions,
                    'form': form,
                }
            )

    form = UserProfileUpdateForm(
        initial=Methods_Users.form_view(request, user, model)
    )
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_PROFILE,
            'title': Users.TITLE,
            'name': Users.NAME,
            'user': user,
            'auth_permissions': auth_permissions,
            'form': form,
        }
    )


def profile_change_password(request):
    template_url = 'users/profile-change-password.html'
    user = Users.login_required(request)
    if user is None:
        Users.set_redirect_field_name(request, request.path)
        return redirect(reverse("users_signin"))
    auth_permissions = Methods_Users.get_auth_permissions(user)
    if settings.ACCESS_PERMISSION_USER_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    model = user
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        form.fields["email"].initial = model.user_username
        if form.is_valid():
            model.user_password_hash = make_password(
                form.cleaned_data['new_password'])
            model.user_password_reset_token = ''
            model.save()
            Methods_Emails.send_info_email(
                request, model.user_username, model.user_name, 'Your password has been updated successfully.')
            messages.info(
                request, 'Your password has been changed successfully.')
            asyncio.run(
                        Methods_Logs.add(
                            settings.MODEL_USERS, 
                            model.user_id, 
                            'User password changed.', 
                            user.user_id, 
                            user.user_name
                        )
                    )
            return redirect(reverse("users_profile_view"))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_PROFILE,
                    'title': Users.TITLE,
                    'name': Users.NAME,
                    'user': user,
                    'auth_permissions': auth_permissions,
                    'form': form,
                }
            )

    form = UserChangePasswordForm()
    form.fields["email"].initial = model.user_username
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_PROFILE,
            'title': Users.TITLE,
            'name': Users.NAME,
            'user': user,
            'auth_permissions': auth_permissions,
            'form': form,
        }
    )
