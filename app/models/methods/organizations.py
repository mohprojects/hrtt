import asyncio
import json

from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.organizations import Organizations
from app.models.methods.logs import Methods_Logs
from app.models.users import Users
from app.models.levels import Levels
from app.utils import Utils


class Methods_Organizations:
    @classmethod
    def format_view(cls, request, user: Users, model: Organizations):
        model.organization_created_at = (
            Utils.get_convert_datetime(
                model.organization_created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.organization_updated_at = (
            Utils.get_convert_datetime(
                model.organization_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        try:
            user = Users.objects.get(pk=model.organization_created_by)
            model.organization_created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.organization_updated_by)
            model.organization_updated_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            categories = model.organization_category
            resp = "<div class='center-block' style='text-left: center;list-style: square;' >"
            categories = categories.strip('][')
            if len(categories) > 0:
                res = ""
                categories = categories.split(',')
                for status in categories:
                    if status:
                        res = res + "<span class='badge badge-light'>"+ ' '.join(str(e) for e in status.strip(' ').strip("'").split('_')) + "</span>"
                resp = resp + res + "</div>"
            if len(categories) <= 0:
                resp = "Not Applicable"
            model.organization_category = mark_safe(str(resp))
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            print('')

        try:
            type = Levels.objects.get(
                pk=model.organization_type)
            model.organization_type = mark_safe(
                str(type.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print('')
            model.organization_type = "Not Applicable"

        try:
            sub_type = Levels.objects.get(
                pk=model.organization_sub_type)
            model.organization_sub_type = mark_safe(
                str(sub_type.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print('')
            model.organization_sub_type = "Not Applicable"

        try:
            financial_agent_class = Levels.objects.get(
                pk=model.organization_financial_agent_class)
            model.organization_financial_agent_class = mark_safe(
                str(financial_agent_class.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            model.organization_financial_agent_class = "Not Applicable"

        try:
            financial_agent_sub_class = Levels.objects.get(
                pk=model.organization_financial_agent_sub_class)
            model.organization_financial_agent_sub_class = mark_safe(
                str(financial_agent_sub_class.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            model.organization_financial_agent_sub_class = "Not Applicable"
            

        try:
            financial_sources_class = Levels.objects.get(
                pk=model.organization_financial_sources_class)
            model.organization_financial_sources_class = mark_safe(
                str(financial_sources_class.level_name) )
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist): 
            model.organization_financial_sources_class = "Not Applicable"   

        try:
            financial_sources_sub_class= Levels.objects.get(
                pk=model.organization_financial_sources_sub_class)
            model.organization_financial_sources_sub_class = mark_safe(str(financial_sources_sub_class.level_name) )
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            model.organization_financial_sources_sub_class = "Not Applicable"

        try:
            financial_schemes_class = Levels.objects.get(
                pk=model.organization_financial_schemes_class)
            model.organization_financial_schemes_class = mark_safe(
                str(financial_schemes_class.level_name) )
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            model.organization_financial_schemes_class = "Not Applicable"   

        try:
            financial_schemes_sub_class= Levels.objects.get(
                pk=model.organization_financial_schemes_sub_class)
            model.organization_financial_schemes_sub_class = mark_safe(str(financial_schemes_sub_class.level_name) )
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            model.organization_financial_schemes_sub_class = "Not Applicable"

        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: Organizations):
        return {
            "name": model.organization_name,
            "email": model.organization_email,
            "type": model.organization_type,
            "sub_type": model.organization_sub_type,
            "phone_number": model.organization_phone_number,
            "category": model.organization_category,
            "financial_agent_class": model.organization_financial_agent_class,
            "financial_agent_sub_class": model.organization_financial_agent_sub_class,
            "financial_schemes_name": model.organization_financial_schemes_name,
            "financial_schemes_class": model.organization_financial_schemes_class,
            "financial_schemes_sub_class": model.organization_financial_schemes_sub_class,
            "financial_sources_class": model.organization_financial_sources_class,
            "financial_sources_sub_class": model.organization_financial_sources_sub_class,
            "healthcare_class": model.organization_healthcare_class,
            "healthcare_sub_class": model.organization_healthcare_sub_class,
        }

    @classmethod
    def validate(cls, request, user: Users, model: Organizations, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Organizations = None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Organizations()

        # name
        if "name" in data:
            model.organization_name = data["name"].strip().title()
        else:
            return True, "Name is required.", model
        try:
            exists = Organizations.objects.get(
                organization_name=model.organization_name
            )
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            exists = None
        if exists is not None:
            return True, "Name is already in use.", model

        # email
        if "email" in data:
            model.organization_email = data["email"]
        else:
            return True, "email is required.", model

        # type
        if "type" in data:
            model.organization_type = data["type"]

        # sub_type
        if "sub_type" in data:
            model.organization_sub_type = data["sub_type"]

        # category
        if "category" in data:
            model.organization_category = data["category"]

        # phone_number
        if "phone_number" in data:
            model.organization_phone_number = data["phone_number"]

        # financial agency class
        if "financial_agent_class" in data:
            model.organization_financial_agent_class = data["financial_agent_class"]
            # financial agent sub class
        if "financial_agent_sub_class" in data:
            model.organization_financial_agent_sub_class = data[
                "financial_agent_sub_class"
            ]
        # financial schemes name
        if "financial_schemes_name" in data:
            model.organization_financial_schemes_name = data["financial_schemes_name"]
        # financial schemes class
        if "financial_schemes_class" in data:
            model.organization_financial_schemes_class = data["financial_schemes_class"]
        # financial schemes sub class
        if "financial_schemes_sub_class" in data:
            model.organization_financial_schemes_sub_class = data[
                "financial_schemes_sub_class"
            ]
        # financial sources class
        if "financial_sources_class" in data:
            model.organization_financial_sources_class = data["financial_sources_class"]
        # financial sources class
        if "financial_sources_sub_class" in data:
            model.organization_financial_sources_sub_class = data[
                "financial_sources_sub_class"
            ]

        # healthcare class
        if "healthcare_class" in data:
            model.organization_healthcare_class = data["healthcare_class"]
            # financial agent sub class
        if "healthcare_sub_class" in data:
            model.organization_healthcare_sub_class = data["healthcare_sub_class"]

        model.organization_created_at = Utils.get_current_datetime_utc()
        model.organization_created_by = user.user_id
        model.organization_updated_at = Utils.get_current_datetime_utc()
        model.organization_updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: Organizations):
        data = json.dumps(data)
        data = json.loads(data)

        # name
        if "name" in data:
            model.organization_name = data["name"].strip().title()
        
        # email
        if "email" in data:
            model.organization_email = data["email"]
        else:
            return True, "email is required.", model

        # type
        if "type" in data:
            model.organization_type = data["type"]
            
        # sub_type
        if "sub_type" in data:
            model.organization_sub_type = data["sub_type"]

        # category
        if "category" in data:
            model.organization_category = data["category"]

        # phone_number
        if "phone_number" in data:
            model.organization_phone_number = data["phone_number"]

        # financial agency class
        if "financial_agent_class" in data:
            model.organization_financial_agent_class = data["financial_agent_class"]

        # financial agent sub class
        if "financial_agent_sub_class" in data:
            model.organization_financial_agent_sub_class = data["financial_agent_sub_class"]

        # financial schemes name
        if "financial_schemes_name" in data:
            model.organization_financial_schemes_name = data["financial_schemes_name"]

        # financial schemes class
        if "financial_schemes_class" in data:
            model.organization_financial_schemes_class = data["financial_schemes_class"]

        # financial schemes sub class
        if "financial_schemes_sub_class" in data:
            model.organization_financial_schemes_sub_class = data["financial_schemes_sub_class"]
        # financial sources class
        if "financial_sources_class" in data:
            model.organization_financial_sources_class = data["financial_sources_class"]

        #financial sources sub class
        if "financial_sources_sub_class" in data:
            model.organization_financial_sources_sub_class = data["financial_sources_sub_class"]

        #healthcare class
        if "healthcare_class" in data:
            model.organization_healthcare_class = data["healthcare_class"]

        #financial agent sub class
        if "healthcare_sub_class" in data:
            model.organization_healthcare_sub_class = data["healthcare_sub_class"]

        model.organization_updated_at = Utils.get_current_datetime_utc()
        model.organization_updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def update_status(cls, request, user: Users, model: Organizations, status):
        model.organization_updated_at = Utils.get_current_datetime_utc()
        model.organization_updated_by = user.user_id
        model.organization_status = status
        model.save()

        asyncio.run(
            Methods_Logs.add(
                settings.MODEL_ORGANIZATIONS,
                model.organization_id,
                "Updated organization status.",
                user.user_id,
                user.user_name,
            )
        )

        return model

    @classmethod
    def delete(cls, request, user: Users, model: Organizations):
        model.delete()
        return True
    
    @classmethod
    def update_levels_type(cls, request, user: Users, model: Organizations, data):
        model.organization_updated_at = Utils.get_current_datetime_utc()
        model.organization_updated_by = user.user_id
        # model.organization_levels_type = data
        model.save()

        asyncio.run(
            Methods_Logs.add(
                settings.MODEL_ORGANIZATIONS,
                model.organization_id,
                "Updated organization levels type.",
                user.user_id,
                user.user_name,
            )
        )

        return model
    
    @classmethod
    def update_levels_status(cls, request, user: Users, model: Organizations, data):
        model.organization_updated_at = Utils.get_current_datetime_utc()
        model.organization_updated_by = user.user_id
        #model.organization_levels_status = data
        model.save()

        asyncio.run(
            Methods_Logs.add(
                settings.MODEL_ORGANIZATIONS,
                model.organization_id,
                "Updated organization levels status.",
                user.user_id,
                user.user_name,
            )
        )

        return model
