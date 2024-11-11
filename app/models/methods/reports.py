import asyncio
import json
from decimal import Decimal
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from app.utils import Utils
from app import settings
from app.models.projects import Projects
from app.models.reports import Reports
from app.models.organizations import Organizations
from app.models.users import Users
from app.models.levels import  Levels
from app.models.methods.logs import Methods_Logs
from app.models.methods.comments import Methods_Comments
from app.models.methods.notifications_reports import Methods_Notifications_Reports


class Methods_Reports:
    @classmethod
    def format_view(cls, request, user: Users, model: Reports):
        model.report_created_at = (
            Utils.get_convert_datetime(
                model.report_created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.report_updated_at = (
            Utils.get_convert_datetime(
                model.report_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        try:
            user = Users.objects.get(pk=model.report_created_by)
            model.report_created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.report_updated_by)
            model.report_updated_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            capital_class= Levels.objects.get(
                pk=model.report_capital_class)
            model.report_capital_class = mark_safe(
                str(capital_class.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print('')

        try:
            capital_sub_class = Levels.objects.get(
                pk=model.report_capital_sub_class)
            model.report_capital_sub_class = mark_safe(
                str(capital_sub_class.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print('')

        try:
            funds_transfer_class = Levels.objects.get(
                pk=model.report_funds_transfer_class)
            model.report_funds_transfer_class = mark_safe(
                str(funds_transfer_class.level_name))
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            print('')
        try:
            financing_agents_ids = model.report_funding_source
            resp = "<div class='center-block' style='text-align: left;list-style: square;' >"
            if financing_agents_ids:
                res = ""
                financing_agents_ids = financing_agents_ids.strip('][').strip(' ').replace("'","").split(',')
                for id in financing_agents_ids:  
                    funding_agent = Organizations.objects.get(pk= int(id))
                    if funding_agent:
                        res = res + "<span class='badge badge-secondary'>"+ funding_agent.organization_name + "</span>"
                resp = resp + res + "</div>"
            model.report_funding_source= mark_safe(
                str(resp) )
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            print('') 

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

        # approve
        if str(model.report_approved_at) != str(0):
            model.report_approved_at = (
                Utils.get_convert_datetime(
                    model.report_approved_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.report_approved_at = ""

        if str(model.report_approved_by) != str(0):
            try:
                user = Users.objects.get(pk=model.report_approved_by)
                model.report_approved_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.report_approved_by = ""

        # deny
        if str(model.report_denied_at) != str(0):
            model.report_denied_at = (
                Utils.get_convert_datetime(
                    model.report_denied_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.report_denied_at = ""
        if str(model.report_denied_by) != str(0):
            try:
                user = Users.objects.get(pk=model.report_denied_by)
                model.report_denied_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.report_denied_by = ""

        try:
            user = Users.objects.get(pk=model.report_created_by)
            model.report_created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        model.report_purchase_value = Utils.format_amount_with_commas(Decimal(model.report_purchase_value))
        model.report_book_value = Utils.format_amount_with_commas(Decimal(model.report_book_value))


        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: Reports):
 
        return {
            "asset_name": model.report_asset_name,
            "capital_class": model.report_capital_class,
            "capital_sub_class": model.report_capital_sub_class,
            "purchase_value": model.report_purchase_value,
            "purchase_currency": model.report_purchase_currency,
            "book_value": model.report_book_value,
            "book_currency": model.report_book_currency,
            "year_purchased": model.report_year_purchased,
            "funding_source": model.report_funding_source,
            "funds_transfer_class": model.report_funds_transfer_class,
            "fiscal_year": model.report_fiscal_year,
        }

    @classmethod
    def validate(cls, request, user: Users, model: Reports, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Reports = None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Reports()

         # project_id
        if "project_id" in data:
            model.project_id = data["project_id"]
        else:
            return True, "project is required.", model

        # asset_name
        if "asset_name" in data:
            model.report_asset_name= data["asset_name"]    
        else:
            return True, "Name is required.", model
        try:
            exists = Reports.objects.get(report_asset_name=data["asset_name"], project_id=data["project_id"])
        except (TypeError, ValueError, OverflowError, Reports.DoesNotExist):
            exists = None
        if exists is not None:
            return True, "An Asset of this name is already registered on this project.", model
        
        if "capital_class" in data:
            model.report_capital_class = data["capital_class"]

        if "capital_sub_class" in data:
            model.report_capital_sub_class = data["capital_sub_class"]


        if "purchase_value" in data:
            model.report_purchase_value = data["purchase_value"]

        if "purchase_currency" in data:
            model.report_purchase_currency = data["purchase_currency"]

        if "book_value" in data:
            model.report_book_value = data["book_value"]
        
        if "book_currency" in data:
            model.report_book_currency = data["book_currency"]

        if "year_purchased" in data:
            model.report_year_purchased = data["year_purchased"]

        if "funding_source" in data:
            model.report_funding_source = data["funding_source"]

        if "funds_transfer_class" in data:
            model.report_funds_transfer_class = data["funds_transfer_class"]

        if "fiscal_year" in data:
            model.report_fiscal_year = data["fiscal_year"]

        model.report_created_at = Utils.get_current_datetime_utc()
        model.report_updated_at = Utils.get_current_datetime_utc()
        
        if user:
            model.report_created_by = user.user_id
            model.report_updated_by = user.user_id

        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users,data, model: Reports):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Reports()

        # asset_name
        if "asset_name" in data:
            model.report_asset_name= data["asset_name"]

        if "capital_class" in data:
            model.report_capital_class = data["capital_class"]

        if "capital_sub_class" in data:
            model.report_capital_sub_class = data["capital_sub_class"]

        if "purchase_value" in data:
            model.report_purchase_value = data["purchase_value"]

        if "purchase_currency" in data:
            model.report_purchase_currency = data["purchase_currency"]

        if "book_value" in data:
            model.report_book_value = data["book_value"]
        
        if "book_currency" in data:
            model.report_book_currency = data["book_currency"]

        if "year_purchased" in data:
            model.report_year_purchased = data["year_purchased"]

        if "funding_source" in data:
            model.report_funding_source = data["funding_source"]
        
        if "funds_transfer_class" in data:
            model.report_funds_transfer_class = data["funds_transfer_class"]

        if "fiscal_year" in data:
            model.report_fiscal_year = data["fiscal_year"]

        model.report_updated_at = Utils.get_current_datetime_utc()
        if user:
            model.report_updated_by = user.user_id
        model.save()
        return False, "Success", model
    
    @classmethod
    def update_status(
        cls,
        request,
        user: Users,
        model: Reports,
        status,
          to,
        comments=None,
    ):
        user_id = 0
        user_name = None
        if user:
            user_id = user.user_id
            user_name = user.user_name

        # submit
        if status == model.STATUS_SUBMITTED and (
            model.report_status == model.STATUS_DRAFT
            or model.report_status == model.STATUS_REJECTED
        ):
            model.report_submitted_at = Utils.get_current_datetime_utc()
            model.report_submitted_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_REPORTS,
                    model.report_id,
                    "Submitted report",
                    user_id,
                    user_name,
                )
            )
            model.report_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": settings.MODEL_REPORTS,
                    "model_id": int(model.report_id),
                    "parent_id": model.STATUS_SUBMITTED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            # notifications
            # subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
            # message = "An report has been submitted by a data reporter."
            # if user:
            #     # send notification to secretary
            #     items = Users.objects.filter(
            #         Q(user_role=Users.TYPE_SUPER_ADMIN)
            #         | Q(user_role=Users.TYPE_ACTIVITY_MANAGER)
            #     ).all()
            #     for item in items:
            #         asyncio.run(
            #             Methods_Notifications_Reports.notify(
            #                 user, "users", item, "users", model, subject, message
            #             )
            #         )
            # else:
            #     items = Users.objects.filter(
            #         Q(user_role=Users.TYPE_SUPER_ADMIN)
            #         | Q(user_role=Users.TYPE_ACTIVITY_MANAGER)
            #     ).all()
            #     for item in items:
            #         asyncio.run(
            #             Methods_Notifications_Reports.notify(
            #                 reporter, "reporters", item, "users", model, subject, message
            #             )
            #         )

            return model

        # accept
        if (
            status == model.STATUS_ACCEPTED
            # and (model.report_status == model.STATUS_SUBMITTED or model.report_status == model.STATUS_DENIED)
        ):
            model.report_accepted_at = Utils.get_current_datetime_utc()
            model.report_accepted_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_REPORTS,
                    model.report_id,
                    "Accepted report",
                    user_id,
                    user_name,
                )
            )
            model.report_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": settings.MODEL_REPORTS,
                    "model_id": int(model.report_id),
                    "parent_id": model.STATUS_ACCEPTED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            # notifications
            # subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
            # message = "An report has been accepted by an report manager."
            # # send notification to editor
            # items = Users.objects.filter(
            #     Q(user_role=Users.TYPE_SUPER_ADMIN)
            # ).all()
            # for item in items:
            #     asyncio.run(
            #         Methods_Notifications_Reports.notify(
            #             user, "users", item, "users", model, subject, message
            #         )
            #     )

            return model

        # reject
        if (
            status == model.STATUS_REJECTED
            and (model.report_status == model.STATUS_SUBMITTED or model.report_status == model.STATUS_DENIED)
        ):
            model.report_rejected_at = Utils.get_current_datetime_utc()
            model.report_rejected_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_REPORTS,
                    model.report_id,
                    "Rejected report",
                    user_id,
                    user_name,
                )
            )
            model.report_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": settings.MODEL_REPORTS,
                    "model_id": int(model.report_id),
                    "parent_id": model.STATUS_REJECTED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            # notifications
            # subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
            # message = "An report has been rejected."
            # # send notification to users
            # items = Users.objects.filter(Q(user_role=Users.TYPE_SUPER_ADMIN)).all()
            # for item in items:
            #     asyncio.run(
            #         Methods_Notifications_Reports.notify(
            #             user, "users", item, "users", model, subject, message
            #         )
            #     )
            # send notification to reporter
            subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
            message = "Your Asset Formation has been rejected."
            items = Users.objects.filter(Q(user_id=model.report_created_by)).all()
            for item in items:
                asyncio.run(
                    Methods_Notifications_Reports.notify(
                        user, "users", item, "users", subject, message
                    )
                )

            return model
        
        # approve
        if (
            status == model.STATUS_APPROVED
            and model.report_status == model.STATUS_ACCEPTED
        ):
            model.report_approved_at = Utils.get_current_datetime_utc()
            model.report_approved_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_REPORTS,
                    model.report_id,
                    "Approved report",
                    user_id,
                    user_name,
                )
            )
            model.report_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": settings.MODEL_REPORTS,
                    "model_id": int(model.report_id),
                    "parent_id": model.STATUS_APPROVED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            # notifications
            subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
            message = "An report has been approved by the Super Admin."
            # send notification to sreport Manager
            items = Users.objects.filter(
                Q(user_role=Users.TYPE_SUPER_ADMIN) | Q(user_role=Users.TYPE_ACTIVITY_MANAGER)
            ).all()
            for item in items:
                asyncio.run(
                    Methods_Notifications_Reports.notify(
                        user, "users", item, "users", model, subject, message
                    )
                )

            return model

        # deny
        if (
            status == model.STATUS_DENIED
            and model.report_status == model.STATUS_ACCEPTED
        ):
            model.report_denied_at = Utils.get_current_datetime_utc()
            model.report_denied_by = user_id
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_REPORTS,
                    model.report_id,
                    "Denied report",
                    user_id,
                    user_name,
                )
            )
            model.report_status = status
            model.save()

            if comments is not None:
                data = {
                    "model": settings.MODEL_REPORTS,
                    "model_id": int(model.report_id),
                    "parent_id": model.STATUS_DENIED,
                    "message": comments,
                    "to":to
                }
                Methods_Comments.create(request, user, data)

            # notifications
            subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
            message = "A Capital Formation has been denied by The Super Admin."
            # send notification to secretary
            # items = Users.objects.filter( Q(user_role=Users.TYPE_ACTIVITY_MANAGER)
            # ).all()
            items = Users.objects.filter(user_id=model.report_accepted_by)
            for item in items:
                asyncio.run(
                    Methods_Notifications_Reports.notify(
                        user, "users", item, "users", model, subject, message
                    )
                )

            return model
        return model

    @classmethod
    def delete(cls, request, user: Users, model: Reports):
        model.delete()
        return True
