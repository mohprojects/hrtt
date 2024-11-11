import asyncio
import json

from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings

from app.models.methods.logs import Methods_Logs
from app.models.currency_rates import Currency_Rates
from app.models.users import Users
from app.utils import Utils


class Methods_Currency_Rates:
    @classmethod
    def format_view(cls, request, user: Users, model: Currency_Rates):
        model.rate_created_at = (
            Utils.get_convert_datetime(
                model.rate_created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.rate_updated_at = (
            Utils.get_convert_datetime(
                model.rate_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        try:
            user = Users.objects.get(pk=model.rate_created_by)
            model.rate_created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.rate_updated_by)
            model.rate_updated_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")
       
        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: Currency_Rates):
        return {
            'currency' : model.rate_currency,
            'rate': model.rate_rate,
            'fiscal_year': model.rate_fiscal_year,
            'currency': model.rate_currency,
            
        }

    @classmethod
    def validate(cls, request, user: Users, model: Currency_Rates, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Currency_Rates = None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Currency_Rates()

        # currency
        if "currency" in data:
            model.rate_currency = data["currency"]

        # rate
        if "rate" in data:
            model.rate_rate = data["rate"]
        
        # fiscal_year
        if 'fiscal_year' in data:
            model.rate_fiscal_year= data['fiscal_year']

        #currency
        if "currency" in data:
            model.rate_currency= data["currency"]

        model.rate_created_at = Utils.get_current_datetime_utc()
        model.rate_created_by = user.user_id
        model.rate_updated_at = Utils.get_current_datetime_utc()
        model.rate_updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: Currency_Rates):
        data = json.dumps(data)
        data = json.loads(data)

         # currency
        if "currency" in data:
            model.rate_currency = data["currency"]

        # rate
        if "rate" in data:
            model.rate_rate = data["rate"]
        
        # fiscal_year
        if 'fiscal_year' in data:
            model.rate_fiscal_year= data['fiscal_year']

        #currency
        if "currency" in data:
            model.rate_currency= data["currency"]

        model.rate_updated_at = Utils.get_current_datetime_utc()
        model.rate_updated_by = user.user_id
        model.save()
        return False, "Success", model


    @classmethod
    def delete(cls, request, user: Users, model: Currency_Rates):
        model.delete()
        return True
