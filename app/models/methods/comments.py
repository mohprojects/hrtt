import json

from app import settings
from app.models.users import Users
from app.models.comments import Comments
from app.utils import Utils


class Methods_Comments:
    @classmethod
    def format_view(cls, request, user: Users, model: Comments):
        model.comment_updated_at = (
            Utils.get_convert_datetime(
                model.comment_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: Comments):
        return {
            "message": model.comment_message,
        }

    @classmethod
    def validate(cls, request, user: Users, model: Comments, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Comments = None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Comments()
        # model
        if "model" in data:
            model.comment_model = data["model"]
        else:
            return True, "Model is required.", model

        # model_id
        if "model_id" in data:
            model.comment_model_id = data["model_id"]
        else:
            return True, "Model Id is required.", model

        # parent_id
        if "parent_id" in data:
            model.comment_parent_id = data["parent_id"]
        else:
            return True, "Parent Id is required.", model

        # message
        if "message" in data:
            model.comment_message = data["message"]
        else:
            return True, "Message is required.", model

        # section
        if "section" in data:
            model.comment_section = data["section"]

        # To
        if "to" in data:
            model.comment_to = data["to"]


        model.comment_updated_at = Utils.get_current_datetime_utc()

        if user is not None:
            model.comment_updated_id = user.user_id
            model.comment_updated_by = user.user_name
            model.comment_updated_by_email = user.user_contact_email_id
            model.comment_updated_by_phone = user.user_contact_phone_number
        else:
            model.comment_updated_id = data["user_id"]
            model.comment_updated_by = data["user_name"]
            model.comment_updated_by_email = data["user_email"]
            model.comment_updated_by_phone = data["user_phone"]
        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: Comments):
        data = json.dumps(data)
        data = json.loads(data)

        # model
        if "model" in data:
            model.comment_model = data["model"]
        else:
            return True, "Model is required.", model

        # model_id
        if "model_id" in data:
            model.comment_model_id = data["model_id"]
        else:
            return True, "Model Id is required.", model

        # parent_id
        if "parent_id" in data:
            model.comment_parent_id = data["parent_id"]
        else:
            return True, "Parent Id is required.", model

        # message
        if "message" in data:
            model.comment_message = data["message"]
        else:
            return True, "Message is required.", model

        # section
        if "section" in data:
            model.comment_section = data["section"]

        # To
        if "to" in data:
            model.comment_to = data["to"]


        model.comment_updated_at = Utils.get_current_datetime_utc()
        model.comment_updated_id = user.user_id
        model.comment_updated_by = user.user_name
        model.save()
        return False, "Success", model

    @classmethod
    def delete(cls, request, user: Users, model: Comments):
        model.delete()
        return True
