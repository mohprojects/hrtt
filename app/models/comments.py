from app import settings
from django.db import models


class Comments(models.Model):
    TITLE = settings.MODEL_COMMENTS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_COMMENTS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    comment_id = models.AutoField(SINGULAR_TITLE + " Id", primary_key=True)
    comment_model = models.CharField("Model", max_length=191, default="")
    comment_model_id = models.CharField("Model Id", max_length=191, default="")
    comment_parent_id = models.IntegerField("Parent", blank=False, default=0)
    comment_message = models.TextField("Message")
    comment_section = models.CharField("Section", max_length=191, default="")
    comment_to = models.IntegerField("To", blank=False, default=0)
    comment_updated_at = models.IntegerField("Updated At", blank=False, default=0)
    comment_updated_id = models.IntegerField("Updated Id", blank=False, default=0)
    comment_updated_by = models.CharField(
        "Updated By", max_length=191, blank=False, default=""
    )
    comment_updated_by_email = models.CharField(
        "Updated By Email", max_length=191, blank=False, default=""
    )
    comment_updated_by_phone = models.CharField(
        "Updated By Phone", max_length=191, blank=False, default=""
    )

    def __unicode__(self):
        return self.comment_id
