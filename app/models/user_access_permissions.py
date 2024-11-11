from django.db import models

from app.models.users import Users
from app.models.access_permissions import Access_Permissions


class User_Access_Permissions(models.Model):
    user_access_permission_id = models.AutoField("Id", primary_key=True)
    users_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    access_permissions_access_permission_name = models.ForeignKey(
        Access_Permissions, on_delete=models.CASCADE
    )
    user_access_permission_updated_at = models.IntegerField(
        "Updated At", blank=False, default=0
    )
    user_access_permission_updated_by = models.IntegerField(
        "Updated By", blank=False, default=0
    )
