from django.db import models

from app import settings
from app.models.methods.status import Methods_Status


class Reports(models.Model):
    TITLE = settings.MODEL_REPORTS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_REPORTS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    TEXT_STATUS_DRAFT = "Draft"
    TEXT_STATUS_SUBMITTED ="Submitted"
    TEXT_STATUS_ACCEPTED = "Accepted"
    TEXT_STATUS_REJECTED = "Rejected"
    TEXT_STATUS_ACTIVE = "Active"
    TEXT_STATUS_APPROVED = "Approved"
    TEXT_STATUS_DENIED = "Denied"

    STATUS_DRAFT = 0
    STATUS_SUBMITTED = 1
    STATUS_ACCEPTED = 2
    STATUS_REJECTED = 3
    STATUS_ACTIVE = 4
    STATUS_APPROVED = 5
    STATUS_DENIED = 6

    ARRAY_STATUS = [
        STATUS_DRAFT,
        STATUS_SUBMITTED,
        STATUS_ACCEPTED,
        STATUS_REJECTED,
        STATUS_ACTIVE,
        STATUS_APPROVED,
        STATUS_DENIED,
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_DRAFT,
        TEXT_STATUS_SUBMITTED,
        TEXT_STATUS_ACCEPTED,
        TEXT_STATUS_REJECTED,
        TEXT_STATUS_ACTIVE,
        TEXT_STATUS_APPROVED,
        TEXT_STATUS_DENIED,
    ]

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
    HTML_TAG_STATUS_ACCEPTED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_ACTIVE_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Accepted <b></div>"
    )
    HTML_TAG_STATUS_REJECTED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_INACTIVE_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Rejected <b></div>"
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

    HTML_TAG_STATUS_APPROVED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_ACTIVE_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Approved <b></div>"
    )
    HTML_TAG_STATUS_DENIED_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_INACTIVE_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Denied <b></div>"
    )


    report_id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    project_id = models.IntegerField("Project", blank=False, default=0)
    report_asset_name = models.CharField('Asset Name', max_length=191, blank=False, default=None)
    report_capital_class = models.CharField('Capital Class', max_length=191, default='')
    report_capital_sub_class = models.CharField('Capital Sub Class', max_length=191, default='')
    report_purchase_value =  models.DecimalField("Purchase Value", max_digits=20, decimal_places=2,default=0.00)
    report_purchase_currency = models.CharField("Purchase Value Currrency", max_length=191, blank=False, default="")
    report_book_value = models.DecimalField("Book Amount", max_digits=20, decimal_places=2,default=0.00)
    report_book_currency = models.CharField("Book Value Currrency", max_length=191, blank=False, default="") 
    report_year_purchased = models.CharField('Year Purchased', max_length=191, blank=False,default='')
    report_funding_source = models.CharField('Funding Source', max_length=191, default='')
    report_funds_transfer_class = models.TextField("Funds Transfer Class", max_length=191, blank=False, default=None)
   # report_funds_transfer_sub_class = models.CharField("Funds Transfer Sub Class", max_length=191, default=None)
    report_fiscal_year = models.CharField("Fiscal Year", max_length=191, blank=False, default=None)
    report_created_at = models.IntegerField('Created At', blank=False, default=0)
    report_created_by = models.IntegerField('Created By', blank=False, default=0)
    report_updated_at = models.IntegerField('Updated At', blank=False, default=0)
    report_updated_by = models.IntegerField('Updated By', blank=False, default=0)
    report_submitted_at = models.IntegerField("Submitted At", blank=False, default=0)
    report_submitted_by = models.IntegerField("Submitted By", blank=False, default=0)
    report_accepted_at = models.IntegerField("Accepted At", blank=False, default=0)
    report_accepted_by = models.IntegerField("Accepted By", blank=False, default=0)
    report_rejected_at = models.IntegerField("Rejected At", blank=False, default=0)
    report_rejected_by = models.IntegerField("Rejected By", blank=False, default=0)
    report_approved_at = models.IntegerField("Approved At", blank=False, default=0)
    report_approved_by = models.IntegerField("Approved By", blank=False, default=0)
    report_denied_at = models.IntegerField("Approved At", blank=False, default=0)
    report_denied_by = models.IntegerField("Approved By", blank=False, default=0)
    report_status = models.IntegerField(
        "Status", blank=False, default=Methods_Status.STATUS_DRAFT
    )

    def __unicode__(self):
        return self.report_id
