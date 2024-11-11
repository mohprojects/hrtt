from django.db import models

from app import settings
from app.models.methods.status import Methods_Status


class Fundings(models.Model):
    TITLE = settings.MODEL_FUNDINGS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_FUNDINGS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    funding_id = models.AutoField(SINGULAR_TITLE + " Id", primary_key=True)
    project_id = models.IntegerField("Project", blank=False, default=0)
    funder_id = models.IntegerField("Funders", blank=False, default=0)
    funding_amount = models.DecimalField("Funded Amount", max_digits=20, decimal_places=2,default=0.00)
    funding_currency = models.CharField("currency", max_length=191, blank=False, default=None)
    funding_created_at = models.IntegerField("Created At", blank=False, default=0)
    funding_created_by = models.IntegerField("Created By", blank=False, default=0)
    funding_updated_at = models.IntegerField("Updated At", blank=False, default=0)
    funding_updated_by = models.IntegerField("Updated By", blank=False, default=0)

    def __unicode__(self):
        return self.funding_id