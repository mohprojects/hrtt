from django.db import models

from app import settings


class Gdp_Populations(models.Model):
    TITLE = settings.MODEL_GDP_POPULATION_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_GDP_POPULATION_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    id = models.AutoField(SINGULAR_TITLE + " Id", primary_key=True)
    fiscal_year = models.CharField(
        "Fiscal Year", max_length=191, blank=False, default=None)
    population = models.BigIntegerField(
        "Total Population", blank=False, default=0)
    budget = models.BigIntegerField(
        "Total Government Budget", blank=False, default=0)
    expenditure = models.BigIntegerField(
        "Total Government Expenditure", blank=False, default=0)
    gdp = models.BigIntegerField("GDP", blank=False, default=0)
    payment_rate = models.DecimalField(
        "Co-Payment Rate", max_digits=3, decimal_places=1, default=0.0)
    expenditure_health = models.BigIntegerField(
        "Government Expenditure on Health", blank=False, default=0)
    budget_health = models.BigIntegerField(
        "Government budget on Health", blank=False, default=0)      

    created_at = models.IntegerField("Created At", blank=False, default=0)
    created_by = models.IntegerField("Created By", blank=False, default=0)
    updated_at = models.IntegerField("Updated At", blank=False, default=0)
    updated_by = models.IntegerField("Updated By", blank=False, default=0)

    def __unicode__(self):
        return self.id
