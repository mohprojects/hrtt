import asyncio
import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app import settings
from app.utils import Utils
from app.models.comments import Comments
from app.models.methods.comments import Methods_Comments
from app.models.methods.logs import Methods_Logs
from app.models.methods.files import Methods_Files
from app.models.methods.users import Methods_Users
from app.models.users import Users
from app.models.activities_inputs import Activities_Inputs
from app.models.reports import Reports
from backend.tables.comments_tables_view import CommentsTableView


class AjaxCommentsListView(View):
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
        # user_notifications = Methods_Users.get_notifications(user)
        # office_user, office_user_uid, office_user_params = Methods_Users.get_office_params(user)

        datatables = request.GET

        model = datatables.get("model")
        modelId = int(datatables.get("model_id"))
        section = datatables.get("section")
        userId = datatables.get("user_id")

        # item draw
        draw = int(datatables.get("draw"))
        # item start
        start = int(datatables.get("start"))
        # item length (limit)
        length = int(datatables.get("length"))
        # item data search
        # search = datatables.get('search[value]')

        # Get objects

        
        objects = Comments.objects
       
        if model == "activities_inputs":
            if user.user_role == Users.TYPE_SUPER_ADMIN:
                objects = objects.filter(Q(comment_model=model) & Q(comment_model_id=modelId) & (
                    Q(comment_parent_id=Activities_Inputs.STATUS_BUDGET_ACCEPTED)|
                    Q(comment_parent_id=Activities_Inputs.STATUS_EXPENSES_ACCEPTED)|
                    Q(comment_parent_id=Activities_Inputs.STATUS_BUDGET_APPROVED)|
                    Q(comment_parent_id=Activities_Inputs.STATUS_EXPENSES_APPROVED)|
                    Q(comment_parent_id=Activities_Inputs.STATUS_BUDGET_DENIED)|
                    Q(comment_parent_id=Activities_Inputs.STATUS_EXPENSES_DENIED)

                ))
            else:
                objects = objects.filter(Q(comment_model=model) & Q(comment_model_id=modelId) & (Q(comment_to=user.user_id)|Q(comment_updated_id= user.user_id)))

        if model == "Reports":
            if user.user_role == Users.TYPE_SUPER_ADMIN:
                objects = objects.filter(Q(comment_model=model) & Q(comment_model_id=modelId) & (
                    Q(comment_parent_id=Reports.STATUS_ACCEPTED)| 
                    Q(comment_parent_id=Reports.STATUS_APPROVED)|
                    Q(comment_parent_id=Reports.STATUS_DENIED)
            ))
            else:
                objects = objects.filter(Q(comment_model=model) & Q(comment_model_id=modelId) & (Q(comment_to=user.user_id)|Q(comment_updated_id= user.user_id)))

            


           
            # else:
            #     objects = objects.filter(Q(comment_model=model) & Q(comment_model_id=modelId) & (Q(comment_to=user.user_id)|Q(comment_updated_id= user.user_id)))
           
    
        # Set record total
        records_total = objects.all().count()
        # Set records filtered
        records_filtered = records_total

        objects = objects.order_by("-comment_id")

        objects_filter = False

        if objects_filter:
            records_filtered = objects.all().count()

        items = objects.all()

        if length == -1:
            paginator = Paginator(items, items.count())
            page_number = 1
        else:
            paginator = Paginator(items, length)
            page_number = start / length + 1

        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(1).object_list

        counter = 0
        data = []
        for record in object_list:
            counter = counter + 1
            value1 = CommentsTableView.render_comment_message(record)
            value2 = CommentsTableView.render_comment_section(record)
            # value3 = CommentsTableView.render_comment_attachment(record)
            value4 = CommentsTableView.render_comment_updated_at(record)
            value5 = CommentsTableView.render_comment_updated_by(record)

            data.append(
                {
                    "comment_message": value1,
                    "comment_section": value2,
                    # "comment_attachment": value3,
                    "comment_parent_id": record.comment_parent_id,
                    "comment_updated_at": value4,
                    "comment_updated_by": value5,
                }
            )

        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }


@csrf_exempt
def create(request):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    auth_permissions = Methods_Users.get_auth_permissions(user)
    print(auth_permissions)
    # user_notifications = Methods_Users.get_notifications(user)
    # office_user, office_user_uid, office_user_params = Methods_Users.get_office_params(user)
    if settings.ACCESS_PERMISSION_COMMENTS_CREATE not in auth_permissions.values():
        return HttpResponseForbidden("Forbidden", content_type="text/plain")

    model = request.POST["model"]
    model_id = request.POST["model_id"]
    parent_id = request.POST["parent_id"]
    message = request.POST["message"]
    section = request.POST["section"]

    if message == "" or model_id == "" or message == "":
        return HttpResponseBadRequest("Bad Request", content_type="text/plain")

    data = {
        "model": model,
        "model_id": int(model_id),
        "parent_id": int(parent_id),
        "message": message,
        "section": section,
    }
    err, msg, model = Methods_Comments.create(request, user, data)
    if err:
        return HttpResponseServerError(msg, content_type="text/plain")
    # messages.success(request, 'Created successfully.')
    asyncio.run(
        Methods_Logs.add(
            settings.MODEL_COMMENTS,
            model.comment_id,
            "Created comments.",
            user.user_id,
            user.user_name,
        )
    )

    return HttpResponse("success", content_type="text/plain")
