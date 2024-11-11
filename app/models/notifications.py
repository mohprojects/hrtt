from app import settings
from django.db import models


class Notifications:
    TITLE = settings.MODEL_NOTIFICATIONS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_NOTIFICATIONS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    _id = models.CharField("Id", max_length=191)
    fr = models.CharField("Fr", max_length=191)
    to = models.CharField("To", max_length=191)
    type = models.CharField("Type", max_length=191)
    model = models.CharField("Model", max_length=191)
    modelId = models.CharField("Model Id", max_length=191)
    message = models.CharField("Message", max_length=191)
    updatedAt = models.IntegerField("Updated At", blank=False, default=0)
    updatedBy = models.IntegerField("Updated By", blank=False, default=0)
    readAt = models.IntegerField("Readt At", blank=False, default=0)
    readStatus = models.IntegerField("Read Status", blank=False, default=0)

    def __unicode__(self):
        return self._id
