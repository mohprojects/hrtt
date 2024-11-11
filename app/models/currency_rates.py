from django.db import models

from app import settings
from app.models.methods.status import Methods_Status


class Currency_Rates(models.Model):
    TITLE = settings.MODEL_RATES_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_RATES_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    rate_id = models.AutoField(SINGULAR_TITLE + " Id", primary_key=True)
    rate_fiscal_year = models.CharField("Fiscal Year", max_length=191, blank=False, default=None)
    rate_currency = models.CharField("Currency", max_length=191, blank=False, default=None)
    rate_rate = models.DecimalField("Rate", max_digits=10, decimal_places=2,default=0.00)
    rate_created_at = models.IntegerField("Created At", blank=False, default=0)
    rate_created_by = models.IntegerField("Created By", blank=False, default=0)
    rate_updated_at = models.IntegerField("Updated At", blank=False, default=0)
    rate_updated_by = models.IntegerField("Updated By", blank=False, default=0)

    def __unicode__(self):
        return self.rate_id