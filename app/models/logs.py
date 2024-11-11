from app import settings
from django.db import models


class Logs:
    TITLE = settings.MODEL_LOGS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_LOGS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    _id = models.CharField("Id", max_length=191)
    model = models.CharField("Model", max_length=191)
    modelId = models.CharField("Model Id", max_length=191)
    message = models.CharField("Message", max_length=191)
    updatedAt = models.IntegerField("Updated At", blank=False, default=0)
    updatedBy = models.IntegerField("Updated By", blank=False, default=0)
    updatedId = models.CharField("Updated Id", max_length=191)
