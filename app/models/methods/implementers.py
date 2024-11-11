import json

from app import settings
from app.models.users import Users
from app.models.implementers import Implementers
from app.utils import Utils


class Methods_Implementers:
    @classmethod
    def format_view(cls, request, user: Users, model: Implementers):
        model.implementer_updated_at = (
            Utils.get_convert_datetime(
                model.implementer_updated_at,
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
    def form_view(cls, request, user: Users, model: Implementers):
        return {
            "name": model.implementer_name,
        }

    @classmethod
    def validate(cls, request, user: Users, model: Implementers, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Implementers = None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Implementers()

        # name
        if "name" in data:
            model.implementer_name = data["name"].strip().title()
        else:
            return True, "Implementer Name is required.", model
        try:
            exists = Implementers.objects.get(
                implementer_name=model.implementer_name
            )
        except (TypeError, ValueError, OverflowError,Implementers.DoesNotExist):
            exists = None
        if exists is not None:
            return True, "Implementer Name is already in use.", model
        
        model.implementer_updated_at = Utils.get_current_datetime_utc()

        if user is not None:
            model.implementer_created_by = user.user_id
            model.implementer_updated_by = user.user_id
         
        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: Implementers):
        data = json.dumps(data)
        data = json.loads(data)

        # name
        if "name" in data:
            model.implementer_name = data["name"].strip().title()
        else:
            return True, "Implementer Name is required.", model
        try:
            exists = Implementers.objects.get(
                implementer_name=model.implementer_name
            )
        except (TypeError, ValueError, OverflowError,Implementers.DoesNotExist):
            exists = None
        if exists is not None:
            return True, "Implementer Name is already in use.", model


        model.implementer_updated_at = Utils.get_current_datetime_utc()
        model.implementer_updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def delete(cls, request, user: Users, model: Implementers):
        model.delete()
        return True
