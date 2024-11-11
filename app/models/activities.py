from django.db import models

from app import settings
from app.models.methods.status import Methods_Status


class Activities(models.Model):
    TITLE = settings.MODEL_ACTIVITIES_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_ACTIVITIES_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    TEXT_STATUS_DRAFT = "Draft"
    TEXT_STATUS_SUBMITTED = "Submitted"
    TEXT_STATUS_BUDGET_ACCEPTED = "Budget Reviewed"
    TEXT_STATUS_BUDGET_REJECTED = "Budget Rejected"
    TEXT_STATUS_BUDGET_APPROVED = "Budget Approved"
    TEXT_STATUS_BUDGET_DENIED = "Budget Denied"
    TEXT_STATUS_EXPENSES_ACCEPTED = "Expenditure  Reviewed"
    TEXT_STATUS_EXPENSES_REJECTED = "Expenditure Rejected"
    TEXT_STATUS_EXPENSES_APPROVED = "Expenditure Approved"
    TEXT_STATUS_EXPENSES_DENIED = "Expenditure Denied"
    TEXT_STATUS_ACTIVE = "Active"
    TEXT_STATUS_BLOCKED = "Blocked"
    STATUS_DRAFT = 0
    STATUS_SUBMITTED = 1
    STATUS_BUDGET_ACCEPTED = 2
    STATUS_BUDGET_APPROVED = 3
    STATUS_EXPENSES_ACCEPTED = 4
    STATUS_EXPENSES_APPROVED = 5
    STATUS_BUDGET_REJECTED = 6
    STATUS_BUDGET_DENIED = 7
    STATUS_EXPENSES_REJECTED = 8
    STATUS_EXPENSES_DENIED = 9
    STATUS_ACTIVE = 10
    STATUS_BLOCKED = 11

    ARRAY_STATUS = [
        STATUS_DRAFT,
        STATUS_SUBMITTED,
        STATUS_BUDGET_ACCEPTED,
        STATUS_BUDGET_APPROVED,
        STATUS_EXPENSES_ACCEPTED,
        STATUS_EXPENSES_APPROVED,
        STATUS_BUDGET_REJECTED,
        STATUS_BUDGET_DENIED,
        STATUS_EXPENSES_REJECTED,
        STATUS_EXPENSES_DENIED,
        STATUS_ACTIVE,
        STATUS_BLOCKED,
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_DRAFT,
        TEXT_STATUS_SUBMITTED,
        TEXT_STATUS_BUDGET_ACCEPTED,
        TEXT_STATUS_BUDGET_APPROVED,
        TEXT_STATUS_EXPENSES_ACCEPTED,
        TEXT_STATUS_EXPENSES_APPROVED,
        TEXT_STATUS_BUDGET_REJECTED,
        TEXT_STATUS_BUDGET_DENIED,
        TEXT_STATUS_EXPENSES_REJECTED,
        TEXT_STATUS_EXPENSES_DENIED,
        TEXT_STATUS_ACTIVE,
        TEXT_STATUS_BLOCKED,
    ]

    # DROPDOWN_STATUS = (
    #     ("", "--select--"),
    #     (STATUS_DRAFT, TEXT_STATUS_DRAFT),
    #     (STATUS_SUBMITTED, TEXT_STATUS_SUBMITTED),
    #     (STATUS_BUDGET_ACCEPTED, TEXT_STATUS_BUDGET_ACCEPTED),
    #     (STATUS_BUDGET_APPROVED, TEXT_STATUS_BUDGET_APPROVED),
    #     (STATUS_EXPENSES_ACCEPTED, TEXT_STATUS_EXPENSES_ACCEPTED),
    #     (STATUS_EXPENSES_APPROVED, TEXT_STATUS_EXPENSES_APPROVED),
    #     (STATUS_BUDGET_REJECTED, TEXT_STATUS_BUDGET_REJECTED),
    #     (STATUS_BUDGET_DENIED, TEXT_STATUS_BUDGET_DENIED),
    #     (STATUS_EXPENSES_REJECTED, TEXT_STATUS_EXPENSES_REJECTED),
    #     (STATUS_EXPENSES_DENIED, TEXT_STATUS_EXPENSES_DENIED),
    #     (STATUS_BLOCKED, TEXT_STATUS_BLOCKED),
    # )

    HTML_TAG_STATUS_DRAFT_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_UNVERIFIED_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Draft <b></div>"
    )
    HTML_TAG_STATUS_SUBMITTED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_UNAPPROVED_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Submitted <b></div>"
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

    HTML_TAG_STATUS_BUDGET_ACCEPTED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_UNDER_REVIEW
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Budget Reviewed <b></div>"
    )
    HTML_TAG_STATUS_BUDGET_APPROVED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_ACTIVE_COLOR
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Budget Approved <b></div>"
    )
    HTML_TAG_STATUS_EXPENSES_ACCEPTED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_UNDER_REVIEW
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Expenditure  Reviewed<b></div>"
    )
    HTML_TAG_STATUS_EXPENSES_APPROVED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_ACTIVE_COLOR
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Expenditure Approved <b></div>"
    )
    HTML_TAG_STATUS_BLOCKED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_BLOCKED_COLOR
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Blocked <b></div>"
    )

    HTML_TAG_STATUS_EXPENSES_REJECTED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_INACTIVE_COLOR
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Expenses Rejected <b></div>"
    )
    HTML_TAG_STATUS_BUDGET_REJECTED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_INACTIVE_COLOR
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Budget Rejected <b></div>"
    )
    HTML_TAG_STATUS_BUDGET_DENIED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_BLOCKED_COLOR
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Blocked <b></div>"
    )
    HTML_TAG_STATUS_EXPENSES_DENIED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_BLOCKED_COLOR
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Blocked <b></div>"
    )


    activity_id = models.AutoField(SINGULAR_TITLE + " Id", primary_key=True)
    organization_id = models.IntegerField("Organization", blank=False, default=0)
    project_id = models.IntegerField("Project", blank=False, default=0)
    activity_name = models.CharField(
        "Name", max_length=1000, blank=False,default=None
    )
    activity_location = models.CharField(
        "Location", max_length=191, blank=False, default=None
    )
    activity_functions = models.CharField("Function", default="", max_length=250)
    activity_sub_functions = models.CharField("Sub Function", default="", max_length=250)
    activity_domain = models.CharField("Domain", max_length=191, blank=False, default=None)
    activity_sub_domain = models.CharField("Sub Domain", max_length=191, blank=False, default="-")
    activity_fiscal_year = models.CharField(
        "Fiscal Year", max_length=191, blank=False, default=None
    )

    activity_created_at = models.IntegerField("Created At", blank=False, default=0)
    activity_created_by = models.IntegerField("Created By", blank=False, default=0)
    activity_updated_at = models.IntegerField("Updated At", blank=False, default=0)
    activity_updated_by = models.IntegerField("Updated By", blank=False, default=0)
    activity_submitted_at = models.IntegerField("Submitted At", blank=False, default=0)
    activity_submitted_by = models.IntegerField("Submitted By", blank=False, default=0)
    activity_accepted_at = models.IntegerField("Accepted At", blank=False, default=0)
    activity_accepted_by = models.IntegerField("Accepted By", blank=False, default=0)
    activity_rejected_at = models.IntegerField("Rejected At", blank=False, default=0)
    activity_rejected_by = models.IntegerField("Rejected By", blank=False, default=0)
    activity_approved_at = models.IntegerField("Approved At", blank=False, default=0)
    activity_approved_by = models.IntegerField("Approved By", blank=False, default=0)
    activity_denied_at = models.IntegerField("Approved At", blank=False, default=0)
    activity_denied_by = models.IntegerField("Approved By", blank=False, default=0)
    activity_status = models.IntegerField(
        "Status", blank=False, default=Methods_Status.STATUS_DRAFT
    )

    def __unicode__(self):
        return self.activity_id
