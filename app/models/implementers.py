from django.db import models

from app import settings
from app.models.methods.status import Methods_Status

class Implementers(models.Model):
    implementer_id = models.AutoField("Id", primary_key=True)
    implementer_name = models.CharField("Implementer Name", max_length=191, blank=False, default="")
    implementer_created_at = models.IntegerField("Created At", blank=False, default=0)
    implementer_created_by = models.IntegerField("Created By", blank=False, default=0)
    implementer_updated_at = models.IntegerField("Updated At", blank=False, default=0)
    implementer_updated_by = models.IntegerField("Updated By", blank=False, default=0)

    def __unicode__(self):
        return self.implementer_id 
    

