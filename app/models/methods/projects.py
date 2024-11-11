import asyncio
import json

from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from django.db.models import Q
from app.models.methods.logs import Methods_Logs
from app.models.organizations import Organizations
from app.models.projects import Projects
from app.models.activities import Activities
from app.models.activities_inputs import Activities_Inputs
from app.models.fundings import Fundings
from app.models.reports import Reports
from app.models.users import Users
from app.utils import Utils
from app.models.levels import Levels
from app.models.implementers import Implementers
from app.models.methods.comments import Methods_Comments
from app.models.methods.notifications_projects import Methods_Notifications_Projects
       

class Methods_Projects:
    @classmethod
    def format_view(cls, request, user: Users, model: Projects):
        model.project_created_at = (
            Utils.get_convert_datetime(
                model.project_created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.project_updated_at = (
            Utils.get_convert_datetime(
                model.project_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        try:
            user = Users.objects.get(pk=model.project_created_by)
            model.project_created_by = mark_safe(
                "<div style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</div>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.project_updated_by)
            model.project_updated_by = mark_safe(
                "<div style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</div>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            organization = Organizations.objects.get(pk=model.organization_id)
            model.organization_id = mark_safe(
                "<div style='text-decoration:underline; color:#1B82DC;' >"
                + str(organization.organization_name)
                + "</div>"
            )
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            model.organization_id = "-"

        
        implementers_ids = model.project_implementer
        resp = "<div class='center-block' style='text-align: left;list-style: square;' >"
        if implementers_ids:
            res = ""
            implementers_ids = implementers_ids.strip('][').strip(' ').replace("'","").split(',')
            for id in implementers_ids:
                if "_" in id:
                    org_impl= id.split('_')
                    if org_impl[0].strip(' ') == 'impl':
                        try:
                            implementer = Implementers.objects.get(pk= int(org_impl[1]))
                            if implementer:
                                res = res + "<span class='badge badge-light'>"+ implementer.implementer_name + "</span>"
                        except (TypeError, ValueError, OverflowError, Implementers.DoesNotExist):
                            print('')
                else:            
                    try: 
                        implementer = Organizations.objects.get(pk= int(id))
                        if implementer:
                            res = res + "<span class='badge badge-light'>"+ implementer.organization_name + "</span>"
                    except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                        print('') 
            resp = resp + res + "</div>"
        model.project_implementer= mark_safe(str(resp) )
        

        try:
            financing_agents_ids = model.project_financing_agent
            resp = "<div class='center-block' style='text-align: left;list-style: square;' >"
            if financing_agents_ids:
                res = ""
                financing_agents_ids = financing_agents_ids.strip('][').strip(' ').replace("'","").split(',')
                for id in financing_agents_ids:  
                    funding_agent = Organizations.objects.get(pk= int(id))
                    if funding_agent:
                        res = res + "<span class='badge badge-secondary'>"+ funding_agent.organization_name + "</span>"
                resp = resp + res + "</div>"
            model.project_financing_agent= mark_safe(
                str(resp) )
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            print('') 


        # assign
        if str(model.project_assigned_at) != str(0):
            model.project_assigned_at = (
                Utils.get_convert_datetime(
                    model.project_assigned_at,
                    settings.TIME_ZONE,
                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
                )
                + " "
                + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
            )
        else:
            model.project_assigned_at = ""

          # assign by
        if str(model.project_assigned_by) != str(0):
            try:
                user = Users.objects.get(pk=model.project_assigned_by)
                model.project_assigned_by = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[user.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(user.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.project_assigned_by = ""
        # assign to
        if str(model.project_assigned_to) != str(0):
            try:
                reporter = Users.objects.get(pk=model.project_assigned_to)
                model.project_assigned_to = mark_safe(
                    "<a href="
                    + reverse("users_view", args=[reporter.pk])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(reporter.user_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                pass
        else:
            model.project_assigned_to = ""

        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: Projects):
        return {
            'organization_id': model.organization_id,
            'name': model.project_name,
            'financing_agent': model.project_financing_agent,
            'implementer': model.project_implementer,
            'start_time': model.project_start_date,
            'deadline' : model.project_deadline,
            'assign_to':model.project_assigned_to
        }

    @classmethod
    def validate(cls, request, user: Users, model: Projects, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Projects = None):
        data = json.dumps(data,indent=4, default=str)
        data = json.loads(data)

        if model is None:
            model = Projects()

        # organization_id
        if "organization_id" in data:
            model.organization_id = data["organization_id"]
        else:
            return True, "Organization is required.", model

        # name
        if "name" in data:
            model.project_name = data["name"].strip().title()
        else:
            return True, "Name is required.", model
        try:
            exists = Projects.objects.get(project_name=model.project_name,organization_id=model.organization_id)
        except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
            exists = None
        if exists is not None:
            return True, "Project's name is already registered on this Organization.", model
        
        # financing_agent
        if 'financing_agent' in data:
            model.project_financing_agent = data['financing_agent']
        else:
            return True, "Financing Agent required.", model

        # implementer
        if "implementer" in data:
            model.project_implementer= data["implementer"]

        # start_time
        if 'start_time' in data:
            model.project_start_date = data['start_time']
        # else:
        #     return True, 'Funder is required.', model
        if 'deadline' in data:
            model.project_deadline = data['deadline']
         
        model.project_created_at = Utils.get_current_datetime_utc()
        model.project_created_by = user.user_id
        model.project_updated_at = Utils.get_current_datetime_utc()
        model.project_updated_by = user.user_id
        model.save()
        
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: Projects):
        data = json.dumps(data,indent=4, default=str)
        data = json.loads(data)

        # organization_id
        if "organization_id" in data:
            model.organization_id = data["organization_id"]

        # name
        if "name" in data:
            model.project_name = data["name"].strip().title()
        # financing_agent
        if 'financing_agent' in data:
            model.project_financing_agent = data['financing_agent']
        # implementer
        if "implementer" in data:
            model.project_implementer= data["implementer"]

        # start_time
        if 'start_time' in data:
            model.project_start_date = data['start_time']
        # else:
        #     return True, 'Funder is required.', model
        if 'deadline' in data:
            model.project_deadline = data['deadline']
            
        if 'assign_to' in data:
            model.project_assigned_to = data['assign_to']

        model.project_updated_at = Utils.get_current_datetime_utc()
        model.project_updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def update_status(cls, request, user: Users, model: Projects, status, comments=None,to=0): 
        user_id = 0
        user_name = None
        if user:
            user_id = user.user_id
            user_name = user.user_name

         # assign
        if status == model.STATUS_ASSIGNED and (
            model.project_status == model.STATUS_DRAFT
            or model.project_status == model.STATUS_ACTIVE
            or model.project_status == model.STATUS_ASSIGNED
        ):
            model.project_assigned_at = Utils.get_current_datetime_utc()
            model.project_assigned_by = user_id
            model.project_assigned_to = to
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_PROJECTS,
                    model.project_id,
                    "Assigned project",
                    user_id,
                    user_name,
                )
            )

            model.project_status = status
            model.save()
           
            # notifications
            subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
            message = f"You have been assigned to work on {model.project_name} project."
            # send notification to reviewer
            items = Users.objects.filter(Q(user_id=model.project_assigned_to)).all()
            for item in items:
                asyncio.run(
                    Methods_Notifications_Projects.notify(
                        user, "users", item, "users", model, subject, message
                    )
                )

            return model
        
        # Active
        if status == model.STATUS_ACTIVE and (
            model.project_status == model.STATUS_ASSIGNED
        ):
            model.project_status = status
            model.save()
            return model
    @classmethod      
    def update_tags(cls,request,model: Projects):
        funding_source = []
        fundings = Fundings.objects.filter(project_id = model.pk)
        for fund in fundings:
            funding_source.append(fund.project_id)

        financing_agents = model.project_financing_agent
        if financing_agents:
            financing_agents = financing_agents.strip('][').strip(' ').replace("'","").split(',')

        merged_list = list(set(funding_source + financing_agents)) 
        model.project_tags = merged_list      
        model.save()
        return model


    @classmethod
    def delete(cls, request, user: Users, model: Projects):
        fundings = Fundings.objects.filter(project_id = model.pk)
        activities = Activities.objects.filter(project_id = model.pk)
        reports   = Reports.objects.filter(project_id = model.pk)
        for funding in fundings:
            funding.delete()
        for activity in activities:
            activity_inputs = Activities_Inputs.objects.filter(activity_id = activity.activity_id)
            for input in activity_inputs:
                input.delete() 
            activity.delete()
        for report in reports:
            report.delete()
        model.delete()
        return True
