from django.db import models

from app import settings
from app.models.methods.status import Methods_Status


class Activities_Inputs(models.Model):
    TITLE = settings.MODEL_ACTIVITIES_INPUTS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_ACTIVITIES_INPUTS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    TEXT_STATUS_DRAFT = "Draft"
    TEXT_STATUS_BUDGET_ACCEPTED = "Budget Reviewed"
    TEXT_STATUS_BUDGET_REJECTED = "Budget Rejected"
    TEXT_STATUS_BUDGET_APPROVED = "Budget Approved"
    TEXT_STATUS_BUDGET_DENIED = "Budget Denied"
    TEXT_STATUS_EXPENSES_ACCEPTED = "Expenditure  Reviewed"
    TEXT_STATUS_EXPENSES_REJECTED = "Expenditure Rejected"
    TEXT_STATUS_EXPENSES_APPROVED = "Expenditure Approved"
    TEXT_STATUS_EXPENSES_DENIED = "Expenditure Denied"

    STATUS_DRAFT = 0
    STATUS_BUDGET_ACCEPTED = 1
    STATUS_BUDGET_APPROVED = 2
    STATUS_EXPENSES_ACCEPTED = 3
    STATUS_EXPENSES_APPROVED = 4
    STATUS_BUDGET_REJECTED = 5
    STATUS_BUDGET_DENIED = 6
    STATUS_EXPENSES_REJECTED = 7
    STATUS_EXPENSES_DENIED = 8

    ARRAY_STATUS = [
        STATUS_DRAFT,
        STATUS_BUDGET_ACCEPTED,
        STATUS_BUDGET_APPROVED,
        STATUS_EXPENSES_ACCEPTED,
        STATUS_EXPENSES_APPROVED,
        STATUS_BUDGET_REJECTED,
        STATUS_BUDGET_DENIED,
        STATUS_EXPENSES_REJECTED,
        STATUS_EXPENSES_DENIED 
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_DRAFT,
        TEXT_STATUS_BUDGET_ACCEPTED,
        TEXT_STATUS_BUDGET_APPROVED,
        TEXT_STATUS_EXPENSES_ACCEPTED,
        TEXT_STATUS_EXPENSES_APPROVED,
        TEXT_STATUS_BUDGET_REJECTED,
        TEXT_STATUS_BUDGET_DENIED,
        TEXT_STATUS_EXPENSES_REJECTED,
        TEXT_STATUS_EXPENSES_DENIED 
    ]
    # DROPDOWN_STATUS = (
    #     ("", "--select--"),
    #     (STATUS_DRAFT, TEXT_STATUS_DRAFT),
    #     (STATUS_BUDGET_ACCEPTED, TEXT_STATUS_BUDGET_ACCEPTED),
    #     (STATUS_BUDGET_APPROVED, TEXT_STATUS_BUDGET_APPROVED),
    #     (STATUS_EXPENSES_ACCEPTED, TEXT_STATUS_EXPENSES_ACCEPTED),
    #     (STATUS_EXPENSES_APPROVED, TEXT_STATUS_EXPENSES_APPROVED),
    #     (STATUS_BUDGET_REJECTED, TEXT_STATUS_BUDGET_REJECTED),
    #     (STATUS_BUDGET_DENIED, TEXT_STATUS_BUDGET_DENIED),
    #     (STATUS_EXPENSES_REJECTED, TEXT_STATUS_EXPENSES_REJECTED),
    #     (STATUS_EXPENSES_DENIED, TEXT_STATUS_EXPENSES_DENIED),
    #)
    
    HTML_TAG_STATUS_DRAFT_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_UNVERIFIED_COLOR
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Draft <b></div>"
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
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Budget Denied <b></div>"
    )
    HTML_TAG_STATUS_EXPENSES_DENIED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_BLOCKED_COLOR
        + ";color:#FFFFFF;width:150px;text-align: center;'><b> Expenditure Denied <b></div>"
    )

    activity_input_id = models.AutoField(" Id", primary_key=True)
    # organization_id = models.IntegerField("Organization", blank=False, default=0)
    # project_id = models.IntegerField("Project", blank=False, default=0)
    activity_id = models.IntegerField("Activity", blank=False, default=0)
    activity_input_class = models.CharField(
        "Input Class", max_length=191, blank=False, default="")
    activity_input_sub_class = models.CharField(
        "Input Sub Class", max_length=191, blank=False, default=""
    )
    activity_input_scheme_class = models.CharField("Financial schemes class", max_length=250, default="")
    activity_input_scheme_sub_class = models.CharField("Financial schemes Sub class", max_length=250, default="")
    activity_input_funder = models.CharField("Funder", max_length=191, blank=False, default="")
    activity_input_funds_transfer_class = models.CharField("Funds Transfer Class", max_length=191, blank=False, default=None)
    activity_input_funds_transfer_sub_class = models.CharField("Funds Transfer Sub Class", max_length=191, blank=False, default=None)
    activity_input_implementer = models.CharField(
        "Implementer", max_length=191, blank=False, default=""
    )
    activity_input_division = models.CharField(
        "Division", max_length=191, blank=False, default=""
    )
    activity_input_budget= models.DecimalField("Budget", max_digits=20, decimal_places=2,default=0.00)
   
    activity_input_budget_currency= models.CharField(
        "Budget Currency", max_length=191, blank=False, default=""
    )
    activity_input_expenses = models.DecimalField("Expenditure", max_digits=20, decimal_places=4,default=0.00)
   
    activity_input_expenses_currency = models.CharField(
        "Expenditure Currency", max_length=191, blank=False, default=""
    )
    # activity_input_fiscal_year = models.CharField(
    #     "Fiscal Year", max_length=191, blank=False, default=None
    # )
    activity_input_double_count = models.IntegerField("Double Count", blank=False, default=0)
    activity_input_created_at = models.IntegerField("Created At", blank=False, default=0)
    activity_input_created_by = models.IntegerField("Created By", blank=False, default=0)
    activity_input_updated_at = models.IntegerField("Updated At", blank=False, default=0)
    activity_input_updated_by = models.IntegerField("Updated By", blank=False, default=0)

    activity_input_budget_accepted_at = models.IntegerField("Budget Accepted At", blank=False, default=0)
    activity_input_budget_accepted_by = models.IntegerField("Budget  Accepted By", blank=False, default=0)
    activity_input_expenses_accepted_at = models.IntegerField("Expenditure Accepted At", blank=False, default=0)
    activity_input_expenses_accepted_by = models.IntegerField("Expenditure Accepted By", blank=False, default=0)

    activity_input_budget_rejected_at = models.IntegerField("Budget  Rejected At", blank=False, default=0)
    activity_input_budget_rejected_by = models.IntegerField("Budget  Rejected By", blank=False, default=0)
    activity_input_expenses_rejected_at = models.IntegerField("Expenditure Rejected At", blank=False, default=0)
    activity_input_expenses_rejected_by = models.IntegerField("Expenditure Rejected By", blank=False, default=0)

    activity_input_budget_approved_at = models.IntegerField("Budget  Approved At", blank=False, default=0)
    activity_input_budget_approved_by = models.IntegerField("Budget Approved By", blank=False, default=0)
    activity_input_expenses_approved_at = models.IntegerField("Expenditure Approved At", blank=False, default=0)
    activity_input_expenses_approved_by = models.IntegerField("Expenditure Approved By", blank=False, default=0)

    activity_input_budget_denied_at = models.IntegerField("Budget Approved At", blank=False, default=0)
    activity_input_budget_denied_by = models.IntegerField("Budget Approved By", blank=False, default=0)
    activity_input_expenses_denied_at = models.IntegerField("Expenditure Approved At", blank=False, default=0)
    activity_input_expenses_denied_by = models.IntegerField("Expenditure Approved By", blank=False, default=0)

    activity_input_status = models.IntegerField(
        "Status", blank=False, default=STATUS_DRAFT 
    )

    def __unicode__(self):
        return self.activity_input_id 
