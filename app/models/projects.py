from django.db import models

from app import settings
from app.models.methods.status import Methods_Status


class Projects(models.Model):
    TITLE = settings.MODEL_PROJECTS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_PROJECTS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    TEXT_STATUS_DRAFT = "Draft"
    TEXT_STATUS_ACTIVE = "Active"
    TEXT_STATUS_ASSIGNED = "Assigned"
    TEXT_STATUS_BLOCKED = "Blocked"

    STATUS_DRAFT = 0
    STATUS_ACTIVE = 1
    STATUS_ASSIGNED = 2
    STATUS_BLOCKED = 3

    ARRAY_STATUS = [
        STATUS_DRAFT,
        STATUS_ASSIGNED,
        STATUS_ACTIVE,
        STATUS_BLOCKED,
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_DRAFT,
        TEXT_STATUS_ACTIVE,
        TEXT_STATUS_ASSIGNED,
        TEXT_STATUS_BLOCKED,
        
    ]
    # DROPDOWN_STATUS = (
    #     ("", "--select--"),
    #     (STATUS_ASSIGNED, TEXT_STATUS_ASSIGNED),
    #     (STATUS_BLOCKED, TEXT_STATUS_BLOCKED),
    #     (STATUS_ACTIVE, TEXT_STATUS_ACTIVE),
    # )

    HTML_TAG_STATUS_DRAFT_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_UNVERIFIED_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Draft <b></div>"
    )
    HTML_TAG_STATUS_ACCEPTED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_ACTIVE_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Accepted <b></div>"
    )

    HTML_TAG_STATUS_ASSIGNED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_UNAPPROVED_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Assigned <b></div>"
    )
    HTML_TAG_STATUS_ACTIVE_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_ACTIVE_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Active <b></div>"
    )
    
    HTML_TAG_STATUS_BLOCKED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_BLOCKED_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Blocked <b></div>"
    )
    project_id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    organization_id = models.IntegerField('Organization', blank=False, default=0)
    # division_id = models.IntegerField('Division', blank=False, default=0)

    project_name = models.CharField('Project Title', max_length=500, blank=False, default=None)
    project_financing_agent = models.CharField('Financing Agent', max_length=250, default='')
    project_implementer = models.CharField('Implementer', max_length=250, default='')
    project_tags = models.CharField('Tags', max_length=250, default='')
    project_start_date = models.DateField(blank=True, null=True)
    project_deadline = models.DateField(blank=True, null=True)
    project_created_at = models.IntegerField('Created At', blank=False, default=0)
    project_created_by = models.IntegerField('Created By', blank=False, default=0)
    project_updated_at = models.IntegerField('Updated At', blank=False, default=0)
    project_updated_by = models.IntegerField('Updated By', blank=False, default=0)
    project_assigned_at = models.IntegerField("Assigned At", blank=False, default=0)
    project_assigned_by = models.IntegerField("Assigned By", blank=False, default=0)
    project_assigned_to = models.IntegerField("Assigned To", blank=False, default=0)
    project_status = models.IntegerField('Status', blank=False, default=STATUS_DRAFT)

    def __unicode__(self):
        return self.project_id
