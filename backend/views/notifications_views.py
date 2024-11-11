import asyncio
import json
import pymongo
from bson import json_util
from django.core.serializers.json import DjangoJSONEncoder
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse

from app import settings
from django.db.models import Q
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.notifications import (Methods_Notifications)
from app.models.methods.notifications_projects import Methods_Notifications_Projects
from app.models.methods.users import Methods_Users
from app.models.users import Users
from app.models. projects import  Projects
from backend.tables.notifications_tables_view import NotificationsTableView


class AjaxNotificationsListView(View):
    def get(self, request):
        user = Users.login_required(request)
        if user is None:
            return HttpResponse(
                json.dumps({}, cls=DjangoJSONEncoder), content_type="application/json"
            )
        items = self._datatables(request, user)
        return HttpResponse(
            json.dumps(items, cls=DjangoJSONEncoder), content_type="application/json"
        )

    def _datatables(self, request, user):
        Methods_Users.get_auth_permissions(user)


        datatables = request.GET

        # item draw
        draw = int(datatables.get("draw"))
        # item start
        start = int(datatables.get("start"))
        # item length (limit)
        length = int(datatables.get("length"))
        # item data search
        # search = datatables.get('search[value]')

       
        cursor = (
            Methods_Mongo.get_collection(settings.MODEL_NOTIFICATIONS)
            .find(
                {
                    "to": user.user_id,
                    "readStatus": Methods_Notifications.STATUS_UNREAD,
                }
            )
            .sort("updatedAt", pymongo.DESCENDING)
        )
        if length == -1:
            items = cursor
        else:
            items = (
                Methods_Mongo.get_collection(settings.MODEL_NOTIFICATIONS)
                .find(
                    {
                        "to": user.user_id,
                        "readStatus": Methods_Notifications.STATUS_UNREAD,
                    }
                )
                .sort("updatedAt", pymongo.DESCENDING)
                .skip(start)
                .limit(length)
            )
        records_total = len(list(cursor))
        records_filtered = records_total

        counter = 0
        data = []
        for item in items:
            record = json.loads(json_util.dumps(item))
            counter = counter + 1
            value0 = NotificationsTableView.render_notification_url(record)
            value1 = NotificationsTableView.render_notification_message(record)
            value2 = NotificationsTableView.render_notification_updated_at(record)
            value3 = NotificationsTableView.render_notification_updated_by(record)

            data.append(
                {
                    "notification_url": value0,
                    "notification_message": value1,
                    "notification_updated_at": value2,
                    "notification_updated_by": value3,
                }
            )

        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }
    

@csrf_exempt
def create(request,project_id):
    
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")

    message = request.POST["notification"]
  
    try:
        model = Projects.objects.get(pk=project_id)
    except (TypeError, ValueError, OverflowError, Projects.DoesNotExist):
        return HttpResponseNotFound("Not Found", content_type="text/plain")
    if message == "":
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")
    subject = settings.APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
    activity_managers = Users.objects.get(Q(user_role=Users.TYPE_ACTIVITY_MANAGER) & Q(organization_id=model.organization_id) & Q(user_id=model.project_created_by))
    data_reporter = Users.objects.get(Q(user_role=Users.TYPE_DATA_REPORTER) & Q(user_id = model.project_assigned_to))
    
    asyncio.run(
        Methods_Notifications_Projects.notify(user,"users",data_reporter,"users",model,subject, message)
        )
    asyncio.run(
        Methods_Notifications_Projects.notify(user,"users",activity_managers,"users",model,subject, message)
        )
    return redirect(reverse("projects_view", args=[project_id]))
