import asyncio
import json

from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings

from app.models.methods.logs import Methods_Logs
from app.models.gdp_populations import Gdp_Populations
from app.models.users import Users
from app.utils import Utils


class Methods_Gdp_Populations:
    @classmethod
    def format_view(cls, request, user: Users, model: Gdp_Populations):
        model.created_at = (
            Utils.get_convert_datetime(
                model.created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.updated_at = (
            Utils.get_convert_datetime(
                model.updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        try:
            user = Users.objects.get(pk=model.created_by)
            model.created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.updated_by)
            model.updated_by = mark_safe(
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
    def form_view(cls, request, user: Users, model: Gdp_Populations):
        return {
            'fiscal_year': model.fiscal_year,
            'population' : model.population,
            'budget' : model.budget,
            'expenditure' : model.expenditure,
            'gdp': model.gdp,
            'payment_rate': model.payment_rate,
            'budget_health' : model.budget_health,
            'expenditure_health' : model.expenditure_health,
        }

    @classmethod
    def validate(cls, request, user: Users, model: Gdp_Populations, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Gdp_Populations = None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Gdp_Populations()

        # fiscal_year
        if 'fiscal_year' in data:
            model.fiscal_year= data['fiscal_year']

        # population
        if "population" in data:
            model.population = data["population"]
        
        # Government budget
        if "budget" in data:
            model.budget= data["budget"]
        
        # Government expenditure
        if "expenditure" in data:
            model.expenditure= data["expenditure"]

        # gdp
        if "gdp" in data:
            model.gdp = data["gdp"]

        # payment_rate
        if "payment_rate" in data:
            model.payment_rate= data["payment_rate"]
            
         # Government budget on health
        if "budget_health" in data:
            model.budget_health= data["budget_health"]
        
        # Government expenditure on health
        if "expenditure_health" in data:
            model.expenditure_health= data["expenditure_health"]

        model.created_at = Utils.get_current_datetime_utc()
        model.created_by = user.user_id
        model.updated_at = Utils.get_current_datetime_utc()
        model.updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: Gdp_Populations):
        data = json.dumps(data)
        data = json.loads(data)

        # fiscal_year
        if 'fiscal_year' in data:
            model.fiscal_year= data['fiscal_year']

        # population
        if "population" in data:
            model.population = data["population"]
        
        # Government budget
        if "budget" in data:
            model.budget= data["budget"]
        
        # Government expenditure
        if "expenditure" in data:
            model.expenditure= data["expenditure"]

        # gdp
        if "gdp" in data:
            model.gdp = data["gdp"]

        # payment_rate
        if "payment_rate" in data:
            model.payment_rate= data["payment_rate"]
            
         # Government budget on health
        if "budget_health" in data:
            model.budget_health= data["budget_health"]
        
        # Government expenditure on health
        if "expenditure_health" in data:
            model.expenditure_health= data["expenditure_health"]

        model.updated_at = Utils.get_current_datetime_utc()
        model.updated_by = user.user_id
        model.save()
        return False, "Success", model
    
    # @classmethod
    # def update_total_budget(cls, request,total_budget, model: Gdp_Populations):
    #     model.budget= total_budget
    #     model.save()
    #     return True

    # @classmethod
    # def update_total_expenditure(cls, request,total_expenses, model: Gdp_Populations):
    #     model.expenditure= total_expenses
    #     model.save()
    #     return True
    @classmethod
    def delete(cls, request, user: Users, model: Gdp_Populations):
        model.delete()
        return True
