from django.db import models

from app import settings


class Files(models.Model):
    TITLE = settings.MODEL_FILES_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_FILES_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    file_id = models.AutoField(SINGULAR_TITLE + " Id", primary_key=True)
    file_model = models.CharField("Model", max_length=191)
    file_model_id = models.CharField("Model Id", max_length=191)
    file_model_no = models.CharField("Model No", max_length=191, default=0)

    file_name = models.CharField("Name", max_length=191)
    file_size = models.BigIntegerField("Size", blank=False, default=0)
    file_type = models.CharField("Type", max_length=191)
    file_mime = models.CharField("Mime", max_length=191)
    file_path = models.CharField("Path", max_length=191)
    file_name_ext = models.CharField("Code", max_length=191)

    file_parent_id = models.IntegerField("Parent Id", blank=False, default=0)
    file_directory_code = models.CharField(
        "Directory Code", max_length=191, blank=False, default=""
    )
    file_directory_name = models.CharField(
        "Directory Name", max_length=191, blank=False, default=""
    )
    file_uploaded_response = models.TextField(
        "Uploaded Response", blank=False, default=""
    )

    file_office_key = models.CharField(
        "Office File Key", max_length=191, blank=False, default=""
    )
    file_office_name = models.CharField(
        "Office File Name", max_length=191, blank=False, default=""
    )
    file_office_type = models.CharField(
        "Office File Type", max_length=191, blank=False, default=""
    )
    file_office_directory_code = models.CharField(
        "Office Directory Code", max_length=191, blank=False, default=""
    )
    file_office_directory_name = models.CharField(
        "Office Directory Name", max_length=191, blank=False, default=""
    )
    file_office_uploaded = models.IntegerField(
        "Office Uploaded", blank=False, default=0
    )
    file_office_uploaded_response = models.TextField(
        "Office Uploaded Response", blank=False, default=""
    )

    file_public = models.BooleanField(default=False)

    file_created_at = models.IntegerField("Created At", blank=False, default=0)
    file_created_id = models.IntegerField("Created Id", blank=False, default=0)
    file_created_by = models.CharField("Created By", max_length=191)

    file_updated_at = models.IntegerField("Updated At", blank=False, default=0)
    file_updated_id = models.IntegerField("Updated Id", blank=False, default=0)
    file_updated_by = models.CharField("Updated By", max_length=191)

    file_deleted_at = models.IntegerField("Deleted At", blank=False, default=0)
    file_deleted_id = models.IntegerField("Deleted Id", blank=False, default=0)
    file_deleted_by = models.CharField(
        "Deleted By", max_length=191, blank=False, default=""
    )

    file_status = models.CharField("Status", max_length=191, blank=False, default="")

    def __unicode__(self):
        return self.file_id
