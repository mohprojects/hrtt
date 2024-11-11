import asyncio
import json
import uuid

from django.template.defaultfilters import filesizeformat
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.files import Files
from app.models.methods.logs import Methods_Logs
from app.models.reports import Reports
from app.models.users import Users
from app.utils import Utils


class Methods_Files:
    @classmethod
    def format_view(cls, request, user: Users, model: Files):
        model.file_created_at = (
            Utils.get_convert_datetime(
                model.file_created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.file_updated_at = (
            Utils.get_convert_datetime(
                model.file_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.file_deleted_at = (
            Utils.get_convert_datetime(
                model.file_deleted_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )

        try:
            user = Users.objects.get(pk=model.file_created_id)
            model.file_created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.file_updated_id)
            model.file_updated_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.file_deleted_id)
            model.file_deleted_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        model.file_size = str(filesizeformat(model.file_size))

        if model.file_model == settings.MODEL_REPORTS:
            try:
                report = Reports.objects.get(pk=model.file_model_id)
                model.file_model_id = mark_safe(
                    "<a href="
                    + reverse("reports_view", args=[model.file_model_id])
                    + " style='text-decoration:underline; color:#1B82DC;' >"
                    + str(report.report_name)
                    + "</a>"
                )
            except (TypeError, ValueError, OverflowError, Reports.DoesNotExist):
                print("")

        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: Files):
        return {
            "name": model.file_name,
            "size": model.file_size,
            "mime": model.file_mime,
            "path": model.file_path,
            "parent_id": model.file_parent_id,
            "directory_code": model.file_directory_code,
            "directory_name": model.file_directory_name,
            "uploaded_response": model.file_uploaded_response,
            "office_name": model.file_office_name,
            "office_type": model.file_office_type,
            "office_directory_code": model.file_office_directory_code,
            "office_directory_name": model.file_office_directory_name,
            "office_uploaded": model.file_office_uploaded,
            "office_uploaded_response": model.file_office_uploaded_response,
        }

    @classmethod
    def validate(cls, request, user: Users, model: Files, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Files = None):
        data = json.dumps(data)
        data = json.loads(data)

        print(data)

        if model is None:
            model = Files()

        # model
        if "model" in data:
            model.file_model = data["model"]
        else:
            return True, "Model is required.", model

        # model_id
        if "model_id" in data:
            model.file_model_id = data["model_id"]
        else:
            return True, "Model Id is required.", model

        # model_no
        if "model_no" in data:
            model.file_model_no = data["model_no"]
        else:
            return True, "Model No is required.", model

        # name
        if "name" in data:
            model.file_name = data["name"]
        else:
            return True, "Name is required.", model

        # size
        if "size" in data:
            model.file_size = data["size"]
        else:
            return True, "Size is required.", model

        # mime
        if "mime" in data:
            model.file_mime = data["mime"]
        else:
            return True, "Mime is required.", model

        # type
        if "type" in data:
            model.file_type = data["type"]
        else:
            return True, "Type is required.", model

        # path
        if "path" in data:
            model.file_path = data["path"]
        else:
            return True, "Path is required.", model

        # name ext
        if "name_ext" in data:
            model.file_name_ext = data["name_ext"]
        else:
            return True, "Name Ext is required.", model

        # parent_id
        if "parent_id" in data:
            model.file_parent_id = data["parent_id"]
        else:
            return True, "Parent Id is required.", model

        # directory_code
        if "directory_code" in data:
            model.file_directory_code = data["directory_code"]
        else:
            return True, "Directory Code is required.", model

        # directory_name
        if "directory_name" in data:
            model.file_directory_name = data["directory_name"]
        else:
            return True, "Directory Name is required.", model

        # uploaded_response
        if "uploaded_response" in data:
            model.file_uploaded_response = data["uploaded_response"]
        else:
            return True, "File Uploaded Response is required.", model

        # office_name
        if "office_name" in data:
            model.file_office_name = data["office_name"]
        else:
            return True, "Office File Name is required.", model

        # office_type
        if "office_type" in data:
            model.file_office_type = data["office_type"]
        else:
            return True, "Office File Type is required.", model

        # office_directory_code
        if "office_directory_code" in data:
            model.file_office_directory_code = data["office_directory_code"]
        else:
            return True, "Office Directory Code is required.", model

        # office_directory_name
        if "office_directory_name" in data:
            model.file_office_directory_name = data["office_directory_name"]
        else:
            return True, "Office Directory Name is required.", model

        # office_uploaded
        if "office_uploaded" in data:
            model.file_office_uploaded = data["office_uploaded"]
        else:
            return True, "Office Uploaded is required.", model

        # office_uploaded_response
        if "office_uploaded_response" in data:
            model.file_office_uploaded_response = data["office_uploaded_response"]
        else:
            return True, "Office Uploaded Response is required.", model

        model.file_created_at = Utils.get_current_datetime_utc()
        model.file_created_id = user.user_id
        model.file_created_by = user.user_name

        model.file_updated_at = Utils.get_current_datetime_utc()
        model.file_updated_id = user.user_id
        model.file_updated_by = user.user_name

        model.file_deleted_at = 0
        model.file_deleted_id = 0
        model.file_deleted_by = ""

        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: Files):
        data = json.dumps(data)
        data = json.loads(data)

        # model
        if "model" in data:
            model.file_model = data["model"]
        else:
            return True, "Model is required.", model

        # model_id
        if "model_id" in data:
            model.file_model_id = data["model_id"]
        else:
            return True, "Model Id is required.", model

        # model_no
        if "model_no" in data:
            model.file_model_no = data["model_no"]
        else:
            return True, "Model No is required.", model

        # name
        if "name" in data:
            model.file_name = data["name"]
        else:
            return True, "Name is required.", model

        # size
        if "size" in data:
            model.file_size = data["size"]
        else:
            return True, "Size is required.", model

        # type
        if "type" in data:
            model.file_type = data["type"]
        else:
            return True, "Type is required.", model

        # mime
        if "mime" in data:
            model.file_mime = data["mime"]
        else:
            return True, "Mime is required.", model

        # path
        if "path" in data:
            model.file_path = data["path"]
        else:
            return True, "Path is required.", model

        # name ext
        if "name_ext" in data:
            model.file_name_ext = data["name_ext"]
        else:
            return True, "Name Ext is required.", model

        # parent_id
        if "parent_id" in data:
            model.file_parent_id = data["parent_id"]
        else:
            return True, "Parent Id is required.", model

        # directory_code
        if "directory_code" in data:
            model.file_directory_code = data["directory_code"]
        else:
            return True, "Directory Code is required.", model

        # directory_name
        if "directory_name" in data:
            model.file_directory_name = data["directory_name"]
        else:
            return True, "Directory Name is required.", model

        # uploaded_response
        if "uploaded_response" in data:
            model.file_uploaded_response = data["uploaded_response"]
        else:
            return True, "File Uploaded Response is required.", model

        # office_name
        if "office_name" in data:
            model.file_office_name = data["office_name"]
        else:
            return True, "Office File Name is required.", model

        # office_type
        if "path" in data:
            model.file_office_type = data["office_type"]
        else:
            return True, "Office File Type is required.", model

        # office_directory_code
        if "office_directory_code" in data:
            model.file_office_directory_code = data["office_directory_code"]
        else:
            return True, "Office Directory Code is required.", model

        # office_directory_name
        if "office_directory_name" in data:
            model.file_office_directory_name = data["office_directory_name"]
        else:
            return True, "Office Directory Name is required.", model

        # office_uploaded
        if "office_uploaded" in data:
            model.file_office_uploaded = data["office_uploaded"]
        else:
            return True, "Office Uploaded is required.", model

        # office_uploaded_response
        if "office_uploaded_response" in data:
            model.file_office_uploaded_response = data["office_uploaded_response"]
        else:
            return True, "Office Uploaded Response is required.", model

        model.file_updated_at = Utils.get_current_datetime_utc()
        model.file_updated_id = user.user_id
        model.file_updated_by = user.user_name

        model.save()
        return False, "Success", model

    @classmethod
    def update_status(cls, request, user: Users, model: Files, status):
        if status == "public":
            model.file_updated_at = Utils.get_current_datetime_utc()
            model.file_updated_by = user.user_id
            model.file_public = True
            model.save()
            message = "Updated file to public."
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_FILES,
                    model.file_id,
                    message,
                    user.user_id,
                    user.user_name,
                )
            )
            return model
        if status == "private":
            model.file_updated_at = Utils.get_current_datetime_utc()
            model.file_updated_by = user.user_id
            model.file_public = False
            model.save()
            message = "Updated file to private."
            asyncio.run(
                Methods_Logs.add(
                    settings.MODEL_FILES,
                    model.file_id,
                    message,
                    user.user_id,
                    user.user_name,
                )
            )
            return model

        return model

    @classmethod
    def delete(cls, request, user: Users, model: Files):
        model.delete()
        # model.file_deleted_at = Utils.get_current_datetime_utc()
        # model.file_deleted_id = user.user_id
        # model.file_deleted_by = user.user_name

        # model.save()
        return True

    @classmethod
    def generate_uuid(cls, attribute):
        token = ""
        unique_token_found = False
        while not unique_token_found:
            token = str(uuid.uuid4())
            if Files.objects.filter(**{attribute: token}).count() == 0:
                unique_token_found = True
        return token
