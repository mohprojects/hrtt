import asyncio
import json

from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings

from app.models.methods.logs import Methods_Logs
from app.models.organizations import Organizations
from app.models.projects import Projects
from app.models.fundings import Fundings
from app.models.users import Users
from app.utils import Utils


class Methods_Fundings:
    @classmethod
    def format_view(cls, request, user: Users, model: Fundings):
        model.funding_created_at = (
            Utils.get_convert_datetime(
                model.funding_created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.funding_updated_at = (
            Utils.get_convert_datetime(
                model.funding_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        try:
            user = Users.objects.get(pk=model.funding_created_by)
            model.funding_created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.funding_updated_by)
            model.funding_updated_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            project = Projects.objects.get(pk=model.project_id)
            model.project_id = mark_safe(str(project.project_name))
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            model.project_id = "-"

        try:
            organization = Organizations.objects.get(pk=model.funder_id)
            model.funder_id = mark_safe(str(organization.organization_name))
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            model.funder_id = "-"
       

        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: Fundings):
        return {
            'project' : model.project_id,
            'organization': model.funder_id,
            'amount': Utils.format_amount_with_commas(model.funding_amount),
            'currency': model.funding_currency,
            
        }

    @classmethod
    def validate(cls, request, user: Users, model: Fundings, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Fundings = None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Fundings()

        # project
        if "project" in data:
            model.project_id = data["project"]

        # organization
        if "organization" in data:
            model.funder_id = data["organization"]
        
        # amount
        if 'amount' in data:
            model.funding_amount= data['amount']

        #currency
        if "currency" in data:
            model.funding_currency= data["currency"]

        model.funding_created_at = Utils.get_current_datetime_utc()
        model.funding_created_by = user.user_id
        model.funding_updated_at = Utils.get_current_datetime_utc()
        model.funding_updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: Fundings):
        data = json.dumps(data)
        data = json.loads(data)

         # project
        if "project" in data:
            model.project_id = data["project"]

        # organization
        if "organization" in data:
            model.funder_id = data["organization"]
        
        # amount
        if 'amount' in data:
            model.funding_amount= data['amount']

        #currency
        if "currency" in data:
            model.funding_currency= data["currency"]

        model.funding_updated_at = Utils.get_current_datetime_utc()
        model.funding_updated_by = user.user_id
        model.save()
        return False, "Success", model


    @classmethod
    def delete(cls, request, user: Users, model: Fundings):
        model.delete()
        return True
