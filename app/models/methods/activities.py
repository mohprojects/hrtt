import asyncio
import json
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.projects import Projects
from app.models.activities import Activities
from app.models.activities_inputs import Activities_Inputs
from app.models.methods.logs import Methods_Logs
from app.models.methods.comments import Methods_Comments
from app.models.methods.notifications_activities import Methods_Notifications_Activities
from app.models.users import Users
from app.utils import Utils
from app.models.levels import Levels


class Methods_Activities:
    @classmethod
    def format_view(cls, request, user: Users, model: Activities):
        model.activity_created_at = (
            Utils.get_convert_datetime(
                model.activity_created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.activity_updated_at = (
            Utils.get_convert_datetime(
                model.activity_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        # submit
        if str(model.activity_submitted_at) != str(0):
            model.activity_submitted_at = (
                Utils.get_convert_datetime(
                    model.activity_submitted_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_submitted_at = ""

        # accept
        if str(model.activity_accepted_at) != str(0):
            model.activity_accepted_at = (
                Utils.get_convert_datetime(
                    model.activity_accepted_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_accepted_at = ""

        # reject
        if str(model.activity_rejected_at) != str(0):
            model.activity_rejected_at = (
                Utils.get_convert_datetime(
                    model.activity_rejected_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_rejected_at = ""

        # approve
        if str(model.activity_approved_at) != str(0):
            model.activity_approved_at = (
                Utils.get_convert_datetime(
                    model.activity_approved_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_approved_at = ""

        if str(model.activity_approved_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_approved_by)
                model.activity_approved_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_approved_by = ""

        # deny
        if str(model.activity_denied_at) != str(0):
            model.activity_denied_at = (
                Utils.get_convert_datetime(
                    model.activity_denied_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.activity_denied_at = ""
        if str(model.activity_denied_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_denied_by)
                model.activity_denied_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_denied_by = ""

        try:
            user = Users.objects.get(pk=model.activity_created_by)
            model.activity_created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.activity_updated_by)
            model.activity_updated_by = mark_safe(
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
            model.project_id = mark_safe(
                "<a href="
                + reverse("projects_view", args=[model.project_id])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(project.project_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
            model.project_id = "-"

        try:
            location = Levels.objects.get(pk=model.activity_location)
            model.activity_location = mark_safe(str(location.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print("")

        try:
            function = Levels.objects.get(pk=model.activity_functions)
            model.activity_functions = mark_safe(str(function.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print("")

        try:
            sub_function = Levels.objects.get(pk=model.activity_sub_functions)
            model.activity_sub_functions = mark_safe(str(sub_function.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print("")

        try:
            domain = Levels.objects.get(pk=model.activity_domain)
            model.activity_domain = mark_safe(str(domain.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print("")

        try:
            sub_program = Levels.objects.get(pk=model.activity_sub_domain)
            model.activity_sub_domain = mark_safe(str(sub_program.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print("")

        # submit
        if str(model.activity_submitted_by) != str(0):
            try:
                reporter = Users.objects.get(pk=model.activity_submitted_by)
                model.activity_submitted_by = mark_safe(str(reporter.user_name))
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_submitted_by = ""

        # accept
        if str(model.activity_accepted_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_accepted_by)
                model.activity_accepted_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_accepted_by = ""

        # reject
        if str(model.activity_rejected_by) != str(0):
            try:
                user = Users.objects.get(pk=model.activity_rejected_by)
                model.activity_rejected_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.activity_rejected_by = ""

        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: Activities):

        return {
            "project_id": model.project_id,
            "name": model.activity_name,
            "location": model.activity_location,
            "functions": model.activity_functions,
            "sub_functions": model.activity_sub_functions,
            "domain": model.activity_domain,
            "sub_domain": model.activity_sub_domain,
            "fiscal_year": model.activity_fiscal_year,
        }

    @classmethod
    def validate(cls, request, user: Users, model: Activities, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Activities = None):
        data = json.dumps(data)
        data = json.loads(data)
        exists = None
        if model is None:
            model = Activities()

        # organization_id
        if "organization_id" in data:
            model.organization_id = data["organization_id"]
        # project_id
        if "project_id" in data:
            model.project_id = data["project_id"]
        else:
            return True, "project is required.", model
        # name
        if "name" in data:
            model.activity_name = data["name"].strip().title()
        else:
            return True, "Name is required.", model

        if "location" in data:
            model.activity_location = data["location"]

        if "functions" in data:
            model.activity_functions = data["functions"]

        if "sub_functions" in data:
            model.activity_sub_functions = data["sub_functions"]

        if "domain" in data:
            model.activity_domain = data["domain"]

        if "sub_domain" in data:
            model.activity_sub_domain = data["sub_domain"]

        if "fiscal_year" in data:
            model.activity_fiscal_year = data["fiscal_year"]
            
        if "status" in data:
            model.activity_status = data["status"]

        model.activity_created_at = Utils.get_current_datetime_utc()
        model.activity_updated_at = Utils.get_current_datetime_utc()

        if user:
            model.activity_created_by = user.user_id
            model.activity_updated_by = user.user_id

        try:
            exists = Activities.objects.get(
                activity_name=model.activity_name,
                project_id=model.project_id,
                activity_location=model.activity_location,
                activity_functions=model.activity_functions,
                activity_domain=model.activity_domain,
                activity_sub_domain=model.activity_sub_domain,
                activity_fiscal_year=model.activity_fiscal_year,
            )
            model = exists
        except (TypeError, ValueError, OverflowError, Activities.DoesNotExist):
            exists = None

        if exists is not None:
            return True, "This activity is already registered on this project.", model
        else:
            model.save()
            return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: Activities):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Activities()

        # name
        if "name" in data:
            model.activity_name = data["name"].strip().title()

        if "location" in data:
            model.activity_location = data["location"]

        if "functions" in data:
            model.activity_functions = data["functions"]

        if "sub_functions" in data:
            model.activity_sub_functions = data["sub_functions"]

        if "domain" in data:
            model.activity_domain = data["domain"]

        if "sub_domain" in data:
            model.activity_sub_domain = data["sub_domain"]

        if "fiscal_year" in data:
            model.activity_fiscal_year = data["fiscal_year"]

        model.activity_updated_at = Utils.get_current_datetime_utc()
       
        if user:
            model.activity_created_by = user.user_id
            model.activity_updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def update_status(
        cls,
        request,
        user: Users,
        model: Activities,
        status,
        comments=None,
    ):

        user_id = 0
        user_name = None
        if user:
            user_id = user.user_id
            user_name = user.user_name

        # submit
        if status == model.STATUS_SUBMITTED and (
            model.activity_status == model.STATUS_DRAFT
            or model.activity_status == model.STATUS_BUDGET_REJECTED
            or model.activity_status == model.STATUS_EXPENSES_REJECTED
        ):
            model.activity_submitted_at = Utils.get_current_datetime_utc()
            model.activity_submitted_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_ACTIVITIES,
                    model.activity_id,
                    "Submitted activity",
                    user_id,
                    user_name,
                )
            )
            model.activity_status = status
            model.save()


            return model
        activity_inputs = Activities_Inputs.objects.filter(
            activity_id=model.activity_id
        )
        # accept budget
        if status == "budget accept":
            if (
                not activity_inputs.filter(
                    activity_input_status=Activities_Inputs.STATUS_DRAFT
                ).exists()
                and activity_inputs.filter(
                    activity_input_status__contains=Activities_Inputs.STATUS_BUDGET_ACCEPTED
                ).exists()
            ):
                model.activity_status = model.STATUS_BUDGET_ACCEPTED
                model.activity_accepted_at = Utils.get_current_datetime_utc()
                model.activity_accepted_by = user_id
                asyncio.run(
                    Methods_Logs.add(
                        settings.MODEL_ACTIVITIES,
                        model.activity_id,
                        "Accepted activity's budget",
                        user_id,
                        user_name,
                    )
                )

                model.save()
                return model
           
        if status == "budget approve":
            if (
                not activity_inputs.filter(
                    activity_input_status=Activities_Inputs.STATUS_BUDGET_ACCEPTED
                ).exists()
                and activity_inputs.filter(
                    activity_input_status__contains=Activities_Inputs.STATUS_BUDGET_APPROVED
                ).exists()
            ):
                model.activity_accepted_at = Utils.get_current_datetime_utc()
                model.activity_accepted_by = user_id
                asyncio.run(
                    Methods_Logs.add(
                        settings.MODEL_ACTIVITIES,
                        model.activity_id,
                        "Approved activity's budget",
                        user_id,
                        user_name,
                    )
                )
                model.activity_status = model.STATUS_BUDGET_APPROVED
                model.save()
                return model

        if status == "expenses accept":
            if (
                not activity_inputs.filter(
                    activity_input_status=Activities_Inputs.STATUS_BUDGET_APPROVED
                ).exists()
                and activity_inputs.filter(
                    activity_input_status__contains=Activities_Inputs.STATUS_EXPENSES_ACCEPTED
                ).exists()
            ):
                model.activity_accepted_at = Utils.get_current_datetime_utc()
                model.activity_accepted_by = user_id
                asyncio.run(
                    Methods_Logs.add(
                        settings.MODEL_ACTIVITIES,
                        model.activity_id,
                        "Accepted activity's expenses",
                        user_id,
                        user_name,
                    )
                )
                model.activity_status = model.STATUS_EXPENSES_ACCEPTED
                model.save()
                return model

        if status == "expenses approve":
            if (
                not activity_inputs.filter(
                    activity_input_status=Activities_Inputs.STATUS_EXPENSES_ACCEPTED
                ).exists()
                and activity_inputs.filter(
                    activity_input_status__contains=Activities_Inputs.STATUS_EXPENSES_APPROVED
                ).exists()
            ):
                model.activity_accepted_at = Utils.get_current_datetime_utc()
                model.activity_accepted_by = user_id
                asyncio.run(
                    Methods_Logs.add(
                        settings.MODEL_ACTIVITIES,
                        model.activity_id,
                        "Approved activity's expenditure",
                        user_id,
                        user_name,
                    )
                )
                model.activity_status = model.STATUS_EXPENSES_APPROVED
                model.save()
                return model
        return model

    @classmethod
    def delete(cls, request, user: Users, model: Activities):
        model.delete()
        return True
