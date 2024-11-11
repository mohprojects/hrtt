import asyncio
import json

from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings

from app.models.methods.logs import Methods_Logs
from app.models.mailing_server_configurations import MailServerConfig
from app.models.users import Users
from app.utils import Utils


class Methods_MailServerConfig:
    @classmethod
    def format_view(cls, request, user: Users, model: MailServerConfig):
        model.created_at = (
            Utils.get_convert_datetime(
                model.created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.updated_at = (
            Utils.get_convert_datetime(
                model.updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        try:
            user = Users.objects.get(pk=model.created_by)
            model.created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")

        try:
            user = Users.objects.get(pk=model.updated_by)
            model.updated_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            print("")
       
        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: MailServerConfig):
        return {
            'host' : model.host,
            'port': model.port,
            'username': model.username,
            'password' : model.password,
            'sender' : model.sender,
            'subject' : model.subject_prefix,
            'tls' : model.tls_enabled,
            'ssl' : model.ssl_enabled
            
        }

    @classmethod
    def validate(cls, request, user: Users, model: MailServerConfig, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: MailServerConfig = None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = MailServerConfig()

        # host
        if "host" in data:
            model.host = data["host"]

        # port
        if "port" in data:
            model.port = data["port"]
        
        # username
        if 'username' in data:
            model.username= data['username']

        # password
        if "password" in data:
            model.password= data["password"]

        # sender
        if "sender" in data:
            model.sender = data["sender"]

        # subject
        if "subject" in data:
            model.subject_prefix = data["subject"]
        
        # tls
        if 'tls' in data:
            model.tls_enabled= data['tls']

        # ssl
        if "ssl" in data:
            model.ssl_enabled = data["ssl"]

        model.created_at = Utils.get_current_datetime_utc()
        model.created_by = user.user_id
        model.updated_at = Utils.get_current_datetime_utc()
        model.updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: MailServerConfig):
        data = json.dumps(data)
        data = json.loads(data)

        # host
        if "host" in data:
            model.host = data["host"]

        # port
        if "port" in data:
            model.port = data["port"]
        
        # username
        if 'username' in data:
            model.username= data['username']

        # Password
        if "password" in data:
            model.password= data["password"]

         # sender
        if "sender" in data:
            model.sender = data["sender"]

        # subject
        if "subject" in data:
            model.subject_prefix = data["subject"]
        
        # tls
        if 'tls' in data:
            model.tls_enabled= data['tls']

        # ssl
        if "ssl" in data:
            model.ssl_enabled = data["ssl"]

        model.updated_at = Utils.get_current_datetime_utc()
        model.updated_by = user.user_id
        model.save()
        return False, "Success", model


    @classmethod
    def delete(cls, request, user: Users, model: MailServerConfig):
        model.delete()
        return True
