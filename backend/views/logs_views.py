import json

import pymongo
from bson import json_util
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.generic import View

from app import settings
from app.models.methods.mongo import Methods_Mongo
from app.models.methods.users import Methods_Users
from app.models.users import Users
from backend.tables.logs_tables_view import LogsTableView


class AjaxLogsListView(View):
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

        model = datatables.get("model")
        model_id = datatables.get("model_id")
        if model_id is not None:
            model_id = int(datatables.get("model_id"))

        # item draw
        draw = int(datatables.get("draw"))
        # item start
        start = int(datatables.get("start"))
        # item length (limit)
        length = int(datatables.get("length"))
        
        cursor = (
            Methods_Mongo.get_collection(settings.MODEL_LOGS)
            .find(
                {
                    "model": model,
                    "modelId": model_id,
                }
            )
            .sort("updatedAt", pymongo.DESCENDING)
        )
        if length == -1:
            items = cursor
        else:
            items = (
                Methods_Mongo.get_collection(settings.MODEL_LOGS)
                .find(
                    {
                        "model": model,
                        "modelId": model_id,
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
            value1 = LogsTableView.render_log_message(record)
            value2 = LogsTableView.render_log_updated_at(record)
            value3 = LogsTableView.render_log_updated_by(record)

            data.append(
                {
                    "log_message": value1,
                    "log_updated_at": value2,
                    "log_updated_by": value3,
                }
            )

        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }
