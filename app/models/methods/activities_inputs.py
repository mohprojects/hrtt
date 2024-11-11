import asyncio
import json
from decimal import Decimal
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings

from app.models.activities import Activities
from app.models.activities_inputs import Activities_Inputs
from app.models.methods.notifications_activities import Methods_Notifications_Activities
from app.models.methods.logs import Methods_Logs
from app.models.methods.comments import Methods_Comments
from app.models.organizations import Organizations
from app.models.users import Users
from app.utils import Utils
from app.models.levels import  Levels
from app.models.implementers import Implementers

class Methods_Activities_Inputs:
    @classmethod
    def format_view(cls, request, user: Users, model: Activities_Inputs):
        model.activity_input_created_at = (
            Utils.get_convert_datetime(
                model.activity_input_created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.activity_input_updated_at = (
            Utils.get_convert_datetime(
                model.activity_input_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

        model.activity_input_budget = Utils.format_amount_with_commas(Decimal(model.activity_input_budget))

        model.activity_input_expenses = Utils.format_amount_with_commas(Decimal(model.activity_input_expenses))

        try:
            user = Users.objects.get(pk=model.activity_input_created_by)
            model.activity_input_created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.activity_input_updated_by)
            model.activity_input_updated_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        # accept budget
        if str(model.activity_input_budget_accepted_at) != str(0):
            model.activity_input_budget_accepted_at = (
                Utils.get_convert_datetime(
                    model.activity_input_budget_accepted_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_input_budget_accepted_at = ""

        if str(model.activity_input_budget_accepted_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_input_budget_accepted_by)
                model.activity_input_budget_accepted_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_input_budget_accepted_by = ""

        # accept expenditure
        if str(model.activity_input_expenses_accepted_at) != str(0):
            model.activity_input_expenses_accepted_at = (
                Utils.get_convert_datetime(
                    model.activity_input_expenses_accepted_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_input_expenses_accepted_at = ""

        if str(model.activity_input_expenses_accepted_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_input_expenses_accepted_by)
                model.activity_input_expenses_accepted_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_input_expenses_accepted_by = ""

        # reject budget
        if str(model.activity_input_budget_rejected_at) != str(0):
            model.activity_input_budget_rejected_at = (
                Utils.get_convert_datetime(
                    model.activity_input_budget_rejected_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_input_budget_rejected_at = ""

        if str(model.activity_input_budget_rejected_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_input_budget_rejected_by)
                model.activity_input_budget_rejected_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_input_budget_rejected_by = ""

        # reject expenditure
        if str(model.activity_input_expenses_rejected_at) != str(0):
            model.activity_input_expenses_rejected_at = (
                Utils.get_convert_datetime(
                    model.activity_input_expenses_rejected_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_input_expenses_rejected_at = ""

        if str(model.activity_input_expenses_rejected_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_input_expenses_rejected_by)
                model.activity_input_expenses_rejected_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_input_expenses_rejected_by = ""

        # approve budget
        if str(model.activity_input_budget_approved_at) != str(0):
            model.activity_input_budget_approved_at = (
                Utils.get_convert_datetime(
                    model.activity_input_budget_approved_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_input_budget_approved_at = ""

        if str(model.activity_input_budget_approved_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_input_budget_approved_by)
                model.activity_input_budget_approved_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_input_budget_approved_by = ""

        # approve Expenditure
        if str(model.activity_input_expenses_approved_at) != str(0):
            model.activity_input_expenses_approved_at = (
                Utils.get_convert_datetime(
                    model.activity_input_expenses_approved_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_input_expenses_approved_at = ""

        if str(model.activity_input_expenses_approved_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_input_expenses_approved_by)
                model.activity_input_expenses_approved_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_input_expenses_approved_by = ""

        # deny budget
        if str(model.activity_input_budget_denied_at) != str(0):
            model.activity_input_budget_denied_at = (
                Utils.get_convert_datetime(
                    model.activity_input_budget_denied_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_input_budget_denied_at = ""
        if str(model.activity_input_budget_denied_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_input_budget_denied_by)
                model.activity_input_budget_denied_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_input_budget_denied_by = ""

        # deny expenditure
        if str(model.activity_input_expenses_denied_at) != str(0):
            model.activity_input_expenses_denied_at = (
                Utils.get_convert_datetime(
                    model.activity_input_expenses_denied_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_input_expenses_denied_at = ""
        if str(model.activity_input_expenses_denied_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_input_expenses_denied_by)
                model.activity_input_expenses_denied_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_input_expenses_denied_by = ""


        try:
            activity = Activities.objects.get(pk=model.activity_id)
            model.activity_id = mark_safe(
                "<a href="
                + reverse("projects_view", args=[model.activity_id])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(activity.activity_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Activities.DoesNotExist):
            model.activity_id = "-"    

        try:
            input= Levels.objects.get(
                pk=model.activity_input_class)
            model.activity_input_class = mark_safe(str(input.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print('')

        try:
            sub_input = Levels.objects.get(
                pk=model.activity_input_sub_class)
            model.activity_input_sub_class = mark_safe(
                str(sub_input.level_name) )
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print('')

        try:
            scheme= Levels.objects.get(
                pk=model.activity_input_scheme_class)
            model.activity_input_scheme_class = mark_safe(str(scheme.level_name) )
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print('')

        try:
            sub_scheme = Levels.objects.get(
                pk=model.activity_input_scheme_sub_class)
            model.activity_input_scheme_sub_class= mark_safe(
                str(sub_scheme.level_name) )
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print('') 

        try:
            funder = Organizations.objects.get(pk= model.activity_input_funder)
            model.activity_input_funder = mark_safe(
                str(funder.organization_name) )
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            print('')

        try:
            transfer_class = Levels.objects.get(
                pk=model.activity_input_funds_transfer_class)
            model.activity_input_funds_transfer_class = mark_safe(
                str(transfer_class.level_name) )
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print('')

        try:
            sub_transfer_class = Levels.objects.get(
                pk=model.activity_input_funds_transfer_sub_class)
            model.activity_input_funds_transfer_sub_class = mark_safe(
                str(sub_transfer_class .level_name) )
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print('')

        
        id = model.activity_input_implementer
        if "_" in id:
            org_impl= id.split('_')
            if org_impl[0].strip(' ') == 'impl':
                try:
                    implementer = Implementers.objects.get(pk= int(org_impl[1]))
                    model.activity_input_implementer = mark_safe(str(implementer.implementer_name))
                except (TypeError, ValueError, OverflowError, Implementers.DoesNotExist):
                    print('')
        else:
            try:
                item= Organizations.objects.get(pk=int(id))
                model.activity_input_implementer = mark_safe(str(item.organization_name))
            except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                print('')

        

        # try:
        #     impl_org = model.activity_input_implementer

        #     implementer = Organizations.objects.get(pk= model.activity_input_implementer)
        #     model.activity_input_implementer = mark_safe(
        #         str(implementer.organization_name) )
        # except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        #     print('')

        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: Activities_Inputs):
 
        return {
            "activity_id": model.activity_id,
            "input_class": model.activity_input_class,
            "input_sub_class": model.activity_input_sub_class,
            "scheme_class" : model.activity_input_scheme_class,
            "scheme_sub_class" : model.activity_input_scheme_sub_class,
            "funder":model.activity_input_funder,
            "transfer_class": model.activity_input_funds_transfer_class,
            "sub_transfer_class": model.activity_input_funds_transfer_sub_class,
            "implementer": model.activity_input_implementer,
            "division": model.activity_input_division,
            "budget": model.activity_input_budget,
            "budget_currency": model.activity_input_budget_currency,
            "expenses":model.activity_input_expenses,
            "expenses_currency": model.activity_input_expenses_currency,
            "double_count": model.activity_input_double_count
            #"fiscal_year": model.activity_input_fiscal_year,
        }

    @classmethod
    def validate(cls, request, user: Users, model: Activities_Inputs, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Activities_Inputs = None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Activities_Inputs()
        if "activity_id" in data:
            model.activity_id = data["activity_id"]
        else:
            return True, "activity is required.", model

        if "input_class" in data:
            model.activity_input_class = data["input_class"]

        if "input_sub_class" in data:
            model.activity_input_sub_class = data["input_sub_class"]

        if "scheme_class" in data:
            model.activity_input_scheme_class = data["scheme_class"]

        if "scheme_sub_class" in data:
            model.activity_input_scheme_sub_class = data["scheme_sub_class"]

        if "funder" in data:
            model.activity_input_funder = data["funder"]
        
        if "transfer_class" in data:
            model.activity_input_funds_transfer_class = data["transfer_class"]

        if "sub_transfer_class" in data:
            model.activity_input_funds_transfer_sub_class = data["sub_transfer_class"]

        if "implementer" in data:
            model.activity_input_implementer = data["implementer"]

        if "division" in data:
            model.activity_input_division = data["division"].strip().title()

        if "budget" in data:
            model.activity_input_budget = data["budget"]

        if "budget_currency" in data:
            model.activity_input_budget_currency = data["budget_currency"]
            
        if "double_count" in data:
            model.activity_input_double_count = data["double_count"]
            
        if "status" in data:
            model.activity_input_status = data["status"]

        model.activity_input_created_at = Utils.get_current_datetime_utc()
        model.activity_input_updated_at = Utils.get_current_datetime_utc()
        
        if user:
            model.activity_input_created_by = user.user_id
            model.activity_input_updated_by = user.user_id 
        if Activities_Inputs.objects.filter(activity_id=model.activity_id,
                                    activity_input_class=model.activity_input_class,
                                    activity_input_sub_class=model.activity_input_sub_class,
                                    activity_input_scheme_class=model.activity_input_scheme_class,
                                    activity_input_scheme_sub_class=model.activity_input_scheme_sub_class,
                                    activity_input_funder=model.activity_input_funder,
                                    activity_input_funds_transfer_class=model.activity_input_funds_transfer_class,
                                    activity_input_funds_transfer_sub_class=model.activity_input_funds_transfer_sub_class,
                                    activity_input_implementer=model.activity_input_implementer,
                                    activity_input_division=model.activity_input_division,
                                    activity_input_budget=model.activity_input_budget,
                                    activity_input_budget_currency=model.activity_input_budget_currency).exists():
            return True, 'Input data already exists in the database.', model
        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users,data, model: Activities_Inputs):
        data = json.dumps(data)
        data = json.loads(data)
        if model is None:
            model = Activities_Inputs()
            
        if "activity_id" in data:
            model.activity_id = data["activity_id"]
        else:
            return True, "activity is required.", model
        # input_class
        if "input_class" in data:
            model.activity_input_class = data["input_class"]

        if "input_sub_class" in data:
            model.activity_input_sub_class = data["input_sub_class"]

        if "scheme_class" in data:
            model.activity_input_scheme_class = data["scheme_class"]

        if "scheme_sub_class" in data:
            model.activity_input_scheme_sub_class = data["scheme_sub_class"]

        if "funder" in data:
            model.activity_input_funder = data["funder"]
        
        if "transfer_class" in data:
            model.activity_input_funds_transfer_class = data["transfer_class"]

        if "sub_transfer_class" in data:
            model.activity_input_funds_transfer_sub_class = data["sub_transfer_class"]

        if "implementer" in data:
            model.activity_input_implementer = data["implementer"]

        if "division" in data:
            model.activity_input_division = data["division"].strip().title()

        if "budget" in data:
            model.activity_input_budget = data["budget"]

        if "budget_currency" in data:
            model.activity_input_budget_currency = data["budget_currency"]

        if "expenses" in data:
            model.activity_input_expenses = data["expenses"]

        if "expenses_currency" in data:
            model.activity_input_expenses_currency = data["expenses_currency"]
            
        if "double_count" in data:
            model.activity_input_double_count = data["double_count"]
            
        if "status" in data:
            model.activity_input_status = data["status"]

        model.activity_input_updated_at = Utils.get_current_datetime_utc()
        if user:
            model.activity_input_updated_by = user.user_id

        try:
            exists = Activities_Inputs.objects.get(activity_id=model.activity_id,
                                    activity_input_class=model.activity_input_class,
                                    activity_input_sub_class=model.activity_input_sub_class,
                                    activity_input_scheme_class=model.activity_input_scheme_class,
                                    activity_input_scheme_sub_class=model.activity_input_scheme_sub_class,
                                    activity_input_funder=model.activity_input_funder,
                                    activity_input_funds_transfer_class=model.activity_input_funds_transfer_class,
                                    activity_input_funds_transfer_sub_class=model.activity_input_funds_transfer_sub_class,
                                    activity_input_implementer=model.activity_input_implementer,
                                    activity_input_division=model.activity_input_division,
                                    activity_input_budget=model.activity_input_budget,
                                    activity_input_budget_currency=model.activity_input_budget_currency,
                                    activity_input_expenses = model.activity_input_expenses)
            model = exists
        except (TypeError, ValueError, OverflowError, Activities_Inputs.DoesNotExist):
            exists = None
        if exists is not None:
             return True, 'Input data already exists in the database.', model
        else:
            model.save()
            return False, "Success", model

    @classmethod
    def update_status(
        cls,
        request,
        user: Users,
        model: Activities_Inputs,
        status,
        to,
        comments=None,
    ):
        user_id = 0
        user_name = None
        if user:
            user_id = user.user_id
            user_name = user.user_name

        activity = Activities.objects.get(activity_id = model.activity_id)

        # accept budget
        if (status == model.STATUS_BUDGET_ACCEPTED and 
            (model.activity_input_status == model.STATUS_DRAFT or model.activity_input_status == model.STATUS_BUDGET_REJECTED)
        ):
            model.activity_input_budget_accepted_at = Utils.get_current_datetime_utc()
            model.activity_input_budget_accepted_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    "activities_inputs",
                    model.activity_input_id,
                    "Accepted activity Input's Budget",
                    user_id,
                    user_name,
                )
            )
            model.activity_input_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": "activities_inputs",
                    "model_id": int(model.activity_input_id),
                    "parent_id": model.STATUS_BUDGET_ACCEPTED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            return model
        
         # accept Expenditure
        if (status == model.STATUS_EXPENSES_ACCEPTED and 
            (model.activity_input_status == model.STATUS_DRAFT or 
             model.activity_input_status == model.STATUS_EXPENSES_REJECTED or
             model.activity_input_status == model.STATUS_BUDGET_REJECTED or
             model.activity_input_status == model.STATUS_BUDGET_ACCEPTED
             )
        ):
            model.activity_input_expenses_accepted_at = Utils.get_current_datetime_utc()
            model.activity_input_expenses_accepted_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    "activities_inputs",
                    model.activity_input_id,
                    "Accepted activity Input's Expenditure",
                    user_id,
                    user_name,
                )
            )
            model.activity_input_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": "activities_inputs",
                    "model_id": int(model.activity_input_id),
                    "parent_id": model.STATUS_EXPENSES_ACCEPTED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            return model

        # reject Budget
        if (status == model.STATUS_BUDGET_REJECTED and 
            (model.activity_input_status == model.STATUS_DRAFT or 
             model.activity_input_status == model.STATUS_EXPENSES_REJECTED or
             model.activity_input_status == model.STATUS_EXPENSES_ACCEPTED or
             model.activity_input_status == model.STATUS_BUDGET_ACCEPTED)
        ):
            model.activity_input_budget_rejected_at = Utils.get_current_datetime_utc()
            model.activity_input_budget_rejected_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    "activities_inputs",
                    model.activity_input_id,
                    "Rejected activity Input'Budget",
                    user_id,
                    user_name,
                )
            )
            model.activity_input_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": "activities_inputs",
                    "model_id": int(model.activity_input_id),
                    "parent_id": model.STATUS_BUDGET_REJECTED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            # send notification to reporter
            subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
            message = f"Your activity {activity.activity_name}'s input budget has been rejected."
            items = Users.objects.filter(user_id=activity.activity_submitted_by)
            for item in items:
                asyncio.run(
                    Methods_Notifications_Activities.notify(
                        user, "users", item, "users", activity, subject, message
                    )
                )
            return model
        
        # reject Expenses
        if (status == model.STATUS_EXPENSES_REJECTED and 
            (model.activity_input_status == model.STATUS_DRAFT or 
             model.activity_input_status == model.STATUS_EXPENSES_ACCEPTED or
             model.activity_input_status == model.STATUS_BUDGET_ACCEPTED)
        ):
            model.activity_input_expenses_rejected_at = Utils.get_current_datetime_utc()
            model.activity_input_expenses_rejected_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    "activities_inputs",
                    model.activity_input_id,
                    "Rejected activity Input'Expenditure",
                    user_id,
                    user_name,
                )
            )
            model.activity_input_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": "activities_inputs",
                    "model_id": int(model.activity_input_id),
                    "parent_id": model.STATUS_EXPENSES_REJECTED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            # send notification to reporter
            subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
            message = f"Your activity {activity.activity_name}'s input Expenditure has been rejected."
            items = Users.objects.filter(user_id=activity.activity_submitted_by)
            for item in items:
                asyncio.run(
                    Methods_Notifications_Activities.notify(
                        user, "users", item, "users", activity, subject, message
                    )
                )

            return model
        
        # approve Budget
        if (
            status == model.STATUS_BUDGET_APPROVED
            and model.activity_input_status == model.STATUS_BUDGET_ACCEPTED
        ):
            model.activity_input_budget_approved_at = Utils.get_current_datetime_utc()
            model.activity_input_budget_approved_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    "activities_inputs",
                    model.activity_input_id,
                    "Approved activity Input 's Budget",
                    user_id,
                    user_name,
                )
            )
            model.activity_input_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": "activities_inputs",
                    "model_id": int(model.activity_input_id),
                    "parent_id": model.STATUS_BUDGET_APPROVED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            return model
        
          # approve Expenditure
        if (
            status == model.STATUS_EXPENSES_APPROVED
            and (model.activity_input_status == model.STATUS_EXPENSES_ACCEPTED or model.activity_input_status == model.STATUS_DRAFT)
        ):
            model.activity_input_expenses_approved_at = Utils.get_current_datetime_utc()
            model.activity_input_expenses_approved_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    "activities_inputs",
                    model.activity_input_id,
                    "Approved activity Input 's Expenses",
                    user_id,
                    user_name,
                )
            )
            model.activity_input_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": "activities_inputs",
                    "model_id": int(model.activity_input_id),
                    "parent_id": model.STATUS_EXPENSES_APPROVED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            return model

        # Deny Budget
        if (
            status == model.STATUS_BUDGET_DENIED
            and model.activity_input_status == model.STATUS_BUDGET_ACCEPTED
        ):
            model.activity_input_budget_denied_at = Utils.get_current_datetime_utc()
            model.activity_input_budget_denied_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    "activities_inputs",
                    model.activity_input_id,
                    "Denied activity Input's Budget",
                    user_id,
                    user_name,
                )
            )
            model.activity_input_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": "activities_inputs",
                    "model_id": int(model.activity_input_id),
                    "parent_id": model.STATUS_BUDGET_DENIED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            # send notification to reporter
            subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
            message = f"The  activity {activity.activity_name}'s input budget has been Denied."
            items = Users.objects.filter(user_id=model.activity_input_budget_accepted_by)
            for item in items:
                asyncio.run(
                    Methods_Notifications_Activities.notify(
                        user, "users", item, "users", activity, subject, message
                    )
                )
            return model
        
        # Deny Expenditure
        if (
            status == model.STATUS_EXPENSES_DENIED
            and model.activity_input_status == model.STATUS_EXPENSES_ACCEPTED
        ):
            model.activity_input_expenses_denied_at = Utils.get_current_datetime_utc()
            model.activity_input_expenses_denied_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    "activities_inputs",
                    model.activity_input_id,
                    "Denied activity Input's Expenditure",
                    user_id,
                    user_name,
                )
            )
            model.activity_input_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": "activities_inputs",
                    "model_id": int(model.activity_input_id),
                    "parent_id": model.STATUS_EXPENSES_DENIED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            # send notification to reporter
            subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
            message = f"The  activity {activity.activity_name}'s input Expenditure has been Denied."
            items = Users.objects.filter(user_id=model.activity_input_expenses_accepted_by)
            for item in items:
                asyncio.run(
                    Methods_Notifications_Activities.notify(
                        user, "users", item, "users", activity, subject, message
                    )
                )
            return model

        return model
    
    @classmethod
    def update_double_count(cls, request, user: Users, model: Activities_Inputs, double_count_value):
        print(f"in Update double count user : {user}  Model : {model}  value : {double_count_value}")
        model.activity_input_updated_at = Utils.get_current_datetime_utc()
        model.activity_input_updated_by = user.user_id
        model.activity_input_double_count = double_count_value
        model.save()

        asyncio.run(
            Methods_Logs.add(
                "activities_inputs",
                model.activity_input_id,
                "Updated activity_input double_count.",
                user.user_id,
                user.user_name,
            )
        )

        return model

    @classmethod
    def delete(cls, request, user: Users, model: Activities_Inputs):
        model.delete()
        return True
