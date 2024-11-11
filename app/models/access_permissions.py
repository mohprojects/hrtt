from django.db import models


class Access_Permissions(models.Model):
    access_permission_name = models.CharField(
        "Access Permission Name",
        primary_key=True,
        max_length=100,
        blank=False,
        unique=True,
    )
    access_permission_details = models.CharField("Details", max_length=255, blank=True)
    access_permission_created_at = models.IntegerField(
        "Created At", blank=False, default=0
    )
    access_permission_updated_at = models.IntegerField(
        "Updated At", blank=False, default=0
    )
