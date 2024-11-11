import asyncio
import json

from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models.levels import Levels
from app.models.methods.logs import Methods_Logs
from app.models.users import Users
from app.utils import Utils


class Methods_Levels:
    @classmethod
    def format_view(cls, request, user: Users, model: Levels):
        model.level_created_at = (
            Utils.get_convert_datetime(
                model.level_created_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        model.level_updated_at = (
            Utils.get_convert_datetime(
                model.level_updated_at,
                settings.TIME_ZONE,
                settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
            )
            + " "
            + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        )
        try:
            user = Users.objects.get(pk=model.level_created_by)
            model.level_created_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            pass

        try:
            user = Users.objects.get(pk=model.level_updated_by)
            model.level_updated_by = mark_safe(
                "<a href="
                + reverse("users_view", args=[user.pk])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(user.user_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            pass

        try:
            level = Levels.objects.get(pk=model.level_parent)
            model.level_parent = mark_safe(
                "<a href="
                + reverse("levels_view", args=[model.level_parent])
                + " style='text-decoration:underline; color:#1B82DC;' >"
                + str(level.level_code) + ': ' +str(level.level_name)
                + "</a>"
            )
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            model.level_parent = "-"

        return model

    @classmethod
    def format_input(cls, request):
        return {}

    @classmethod
    def form_view(cls, request, user: Users, model: Levels):
        return {
            "key": model.level_key,
            "code": model.level_code,
            "name": model.level_name,
            "parent": model.level_parent,            
        }

    @classmethod
    def validate(cls, request, user: Users, model: Levels, new=False):
        return False, "Success", model

    @classmethod
    def create(cls, request, user: Users, data, model: Levels = None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Levels()
        
        # key
        if "code" in data:
            model.level_key = data["key"]
        else:
            return True, "Key is required.", model
        
        # code
        if "code" in data:
            model.level_code = data["code"]
        else:
            return True, "Code is required.", model

        # name
        if "name" in data:
            model.level_name = data["name"].strip().title()
        else:
            return True, "Name is required.", model

        # parent
        if "parent" in data:
            model.level_parent = data["parent"]
        else:
            return True, "Parent is required.", model

        model.level_created_at = Utils.get_current_datetime_utc()
        model.level_created_by = user.user_id
        model.level_updated_at = Utils.get_current_datetime_utc()
        model.level_updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def update(cls, request, user: Users, data, model: Levels):
        data = json.dumps(data)
        data = json.loads(data)

        # key
        if "code" in data:
            model.level_key = data["key"]
        else:
            return True, "Key is required.", model

        # code
        if "code" in data:
            model.level_code = data["code"]
        else:
            return True, "Code is required.", model

        # name
        if "name" in data:
            model.level_name = data["name"].strip().title()
        else:
            return True, "Name is required.", model

        # parent
        if "parent" in data:
            model.level_parent = data["parent"]
        else:
            return True, "Parent is required.", model

        model.level_updated_at = Utils.get_current_datetime_utc()
        model.level_updated_by = user.user_id
        model.save()
        return False, "Success", model

    @classmethod
    def update_status(cls, request, user: Users, model: Levels, status):
        model.level_updated_at = Utils.get_current_datetime_utc()
        model.level_updated_by = user.user_id
        model.level_status = status
        model.save()

        asyncio.run(
            Methods_Logs.add(
                settings.MODEL_LEVELS,
                model.level_id,
                "Updated level status.",
                user.user_id,
                user.user_name,
            )
        )

        return model

    @classmethod
    def delete(cls, request, user: Users, model: Levels):
        model.delete()
        return True
    
    @classmethod
    def tree(cls, request, user: Users, id):
        values = '<ul>'
        try:
            model = Levels.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            values += '</ul>'
            return values
        name = str(model.level_code)+": "+str(model.level_name)
        values += '<li class="jstree-open" data-id="'+str(id)+'">'+name
        children = Levels.objects.filter(
            Q(level_parent=model.level_id)
        ).all()
        if len(children) > 0:
            for child in children:
                values += Methods_Levels.tree(request, user, child.level_id)

        values += '</li></ul>'
        return values
    
    @classmethod
    def tree_create(cls, request, user: Users, id):
        values = '<ul>'
        try:
            model = Levels.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            values += '</ul>'
            return values
        exists = False
        name = str(model.level_code)+": "+str(model.level_name)
        if exists:
            values += '<li class="jstree-open" data-id="'+str(id)+'" data-checkstate="checked">'+name
        else:
            values += '<li class="jstree-open" data-id="'+str(id)+'" >'+name
        children = Levels.objects.filter(
            Q(level_parent=model.level_id)
        ).all()
        if len(children) > 0:
            for child in children:
                values += Methods_Levels.tree_create(request, user, child.level_id)

        values += '</li></ul>'
        return values
    
    @classmethod
    def tree_edit(cls, request, user: Users, id, selected):
        values = '<ul>'
        try:
            model = Levels.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            values += '</ul>'
            return values
        # values += '<li><input id="demo-form-checkbox-'+str(id)+'" class="magic-checkbox" type="checkbox"><label for="demo-form-checkbox-'+str(id)+'">'+str(model.level_code)+': '+str(model.level_name)+'</label>'
        exists = False
        
        try:
            x = selected.index(str(id))
            if x > 0:
                exists = True
        except Exception as e:
            pass
        name = str(model.level_code)+": "+str(model.level_name)
        if exists:
            values += '<li class="jstree-open" data-id="'+str(id)+'" data-checkstate="checked">'+name
        else:
            values += '<li class="jstree-open" data-id="'+str(id)+'" >'+name
        children = Levels.objects.filter(
            Q(level_parent=model.level_id)
        ).all()
        if len(children) > 0:
            for child in children:
                values += Methods_Levels.tree_edit(request, user, child.level_id, selected)

        values += '</li></ul>'
        return values
    
    @classmethod
    def tree_view(cls, request, user: Users, id, selected):
        values = '<ul>'
        try:
            model = Levels.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError, Levels.DoesNotExist):
            values += '</ul>'
            return values
        # values += '<li><input id="demo-form-checkbox-'+str(id)+'" class="magic-checkbox" type="checkbox"><label for="demo-form-checkbox-'+str(id)+'">'+str(model.level_code)+': '+str(model.level_name)+'</label>'
        exists = False
        try:
            x = selected.index(str(id))
            if x > 0:
                exists = True
        except Exception as e:
            pass
        
        children = Levels.objects.filter(
            Q(level_parent=model.level_id)
        ).all()

        name = str(model.level_code)+": "+str(model.level_name)

        if len(children) > 0:
            if exists:
                values += '<li class="jstree-open jstree-disabled" data-id="'+str(id)+'" data-checkstate="checked">'+name
            else:
                values += '<li class="jstree-open jstree-disabled" data-id="'+str(id)+'" data-checkstate="opened">'+name
        else:
            if exists:
                values += '<li class="jstree jstree-disabled" data-id="'+str(id)+'" data-checkstate="checked">'+name
            else:
                values += '<li class="jstree jstree-disabled" data-id="'+str(id)+'" data-checkstate="hidden">'+name

        if len(children) > 0:
            for child in children:
                values += Methods_Levels.tree_edit(request, user, child.level_id, selected)

        if exists:
            values += '</li></ul>'
        else:
            values += '</li></ul>'
        return values
