from django.db import models

from app import settings
from app.models.methods.status import Methods_Status


class Levels(models.Model):
    TITLE = settings.MODEL_LEVELS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_LEVELS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    level_id = models.AutoField(SINGULAR_TITLE + " Id", primary_key=True)
    level_key = models.CharField("Key", max_length=191, blank=False, default=None)
    level_code = models.CharField("Code", max_length=191, blank=False, default=None)
    level_name = models.CharField("Name", max_length=191, blank=False, default=None)
    level_parent = models.IntegerField("Parent", blank=False, default=0)
    level_created_at = models.IntegerField("Created At", blank=False, default=0)
    level_created_by = models.IntegerField("Created By", blank=False, default=0)
    level_updated_at = models.IntegerField("Updated At", blank=False, default=0)
    level_updated_by = models.IntegerField("Updated By", blank=False, default=0)
    level_status = models.IntegerField("Status", blank=False, default=Methods_Status.STATUS_ACTIVE)

    def __unicode__(self):
        return self.level_id
