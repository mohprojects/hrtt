import asyncio
import json

from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.methods.logs import Methods_Logs
from app.models.methods.emails import Methods_Emails
from app.models.user_access_permissions import User_Access_Permissions
from app.models.users import Users
from app.models.organizations import Organizations
#from app.models.divisions import Divisions
from app.utils import Utils


class Methods_Users:
    @classmethod
    def format_view(cls, request, user: Users, model: Users):
        model.user_created_at = (
            Utils.get_convert_datetime(
                model.user_created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.user_updated_at = (
            Utils.get_convert_datetime(
                model.user_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        try:
            user = Users.objects.get(pk=model.user_created_by)
            model.user_created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.user_updated_by)
            model.user_updated_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            organization = Organizations.objects.get(pk=model.organization_id)
            model.organization_id = mark_safe(
                "<a href="
                + reverse("organizations_view", args=[model.organization_id])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(organization.organization_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            model.organization_id = "-"

        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: Users):
        return {
            'email': model.user_username,
            'name': model.user_name,
            'phone_number': model.user_contact_phone_number,
            'organization_id': model.organization_id,
            "first_name": model.user_first_name,
            "middle_name": model.user_middle_name,
            "last_name": model.user_last_name,
            'role': model.user_role,
        }

    @classmethod
    def validate(cls, request, user: Users, model: Users, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Users = None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Users()
            model.user_type = Users.TYPE_OTHER
            model.user_gender = ""

        model.user_auth_key = Users.generate_unique_token(Users, "user_auth_key")
        model.user_password_hash = make_password(data["password"])

        if "name" in data:
            model.user_name = data["name"]
        else:
            model.user_name = ""
        if "phone_number" in data:
            model.user_contact_phone_number = data["phone_number"]
        else:
            model.user_contact_phone_number = ""
        if "email" in data:
            model.user_username = model.user_contact_email_id = data["email"]
        else:
            model.user_username = model.user_contact_email_id = ""
        if "organization_id" in data:
            model.organization_id = data["organization_id"]
        else:
            return True, 'Organization is required.', model
    
        if 'role' in data:
            model.user_role = data['role']
        else:
            model.user_role = ""

        if "first_name" in data:
            model.user_first_name = data["first_name"]
        else:
            model.user_first_name = ''   
        
        if "middle_name" in data:
            model.user_middle_name = data["middle_name"]
        else:
            model.user_middle_name = ""

        if "last_name" in data:
            model.user_last_name = data["last_name"]
        else:
            model.user_last_name =''

        if "first_name" in data:
            model.user_first_name = data["first_name"]
        else:
            model.user_first_name = ''   
        
        if "middle_name" in data:
            model.user_middle_name = data["middle_name"]
        else:
            model.user_middle_name = ""

        if "last_name" in data:
            model.user_last_name = data["last_name"]
        else:
            model.user_last_name =''

        model.user_password_reset_token = ''
        model.user_profile_photo_file_path = ''

        model.user_name = (
            str(model.user_first_name)
            + " "
            + str(model.user_middle_name)
            + " "
            + str(model.user_last_name)
        )

        model.user_created_at = Utils.get_current_datetime_utc()
        if user is not None:
            model.user_created_by = user.user_id
        model.user_updated_at = Utils.get_current_datetime_utc()
        if user is not None:
            model.user_updated_by = user.user_id
        model.user_status = Users.STATUS_UNVERIFIED
        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: Users):
        data = json.dumps(data)
        data = json.loads(data)

        if 'name' in data:
            model.user_name = data['name']
        if 'phone_number' in data:
            model.user_contact_phone_number = data['phone_number']
        if 'email' in data:
            model.user_contact_email_id = data['email']
        if 'organization_id' in data:
            model.organization_id = data['organization_id']
        if 'role' in data:
            model.user_role = data['role']
        if "first_name" in data:
            model.user_first_name = data["first_name"]  
        
        if "middle_name" in data:
            model.user_middle_name = data["middle_name"]

        if "last_name" in data:
            model.user_last_name = data["last_name"]

        model.user_name = (
            str(model.user_first_name)
            + " "
            + str(model.user_middle_name)
            + " "
            + str(model.user_last_name)
        )
       
        model.user_updated_at = Utils.get_current_datetime_utc()
        model.user_updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def update_status(cls, request, user: Users, model: Users, status):
        model.user_updated_at = Utils.get_current_datetime_utc()
        model.user_updated_by = user.user_id
        model.user_status = status
        model.save()

        asyncio.run(
            Methods_Logs.add(
                settings.MODEL_USERS,
                model.user_id,
                "Updated user status.",
                user.user_id,
                user.user_name,
            )
        )

        return model

    @classmethod
    def delete(cls, request, user: Users, model: Users):
        model.delete()
        return True

    @classmethod
    def get_auth_permissions(cls, user: Users):
        user_auth_permissions = User_Access_Permissions.objects.filter(
            users_user_id_id=user.user_id
        )
        auth_permissions = {}
        counter = 0
        for user_auth_permission in user_auth_permissions:
            auth_permissions[
                counter
            ] = user_auth_permission.access_permissions_access_permission_name_id
            counter = counter + 1
        return auth_permissions

