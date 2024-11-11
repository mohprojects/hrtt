from django.db import models
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)

from app import settings
from app.models.methods.status import Methods_Status


class Organizations(models.Model):
    TITLE = settings.MODEL_ORGANIZATIONS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_ORGANIZATIONS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())


    TEXT_STATUS_DRAFT = "Draft"
    TEXT_STATUS_ACTIVE = "Active"
    TEXT_STATUS_INNACTIVE = "Inactive"
    TEXT_STATUS_BLOCKED = "Blocked"

    STATUS_DRAFT = 0
    STATUS_ACTIVE = 1
    STATUS_INNACTIVE = 2

    ARRAY_STATUS = [
        STATUS_DRAFT,
        STATUS_INNACTIVE,
        STATUS_ACTIVE,
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_DRAFT,
        TEXT_STATUS_ACTIVE,
        TEXT_STATUS_INNACTIVE,
        
    ]
    # DROPDOWN_STATUS = (
    #     ("", "--select--"),
    #     (STATUS_INNACTIVE, TEXT_STATUS_INNACTIVE),
    #     (STATUS_ACTIVE, TEXT_STATUS_ACTIVE),
    # )
    #### Types #####
    STATUS_FINANCING = "financing_agent"
    STATUS_HEALTHCARE = "healthcare_provider"
    STATUS_FUNDING = "funding_source"
    STATUS_IMPLEMENTER = "implementer"
 

    DROPDOWN_STATUS_ = [
        (STATUS_FINANCING, (STATUS_FINANCING.title()).replace("_", " ")),
        (STATUS_HEALTHCARE, (STATUS_HEALTHCARE.title()).replace("_", " ")),
        (STATUS_FUNDING , (STATUS_FUNDING .title()).replace("_", " ")),
        (STATUS_IMPLEMENTER, (STATUS_IMPLEMENTER.title()).replace("_", " ")) 
    ]
   
    HTML_TAG_STATUS_INNACTIVE_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_INACTIVE_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Inactive <b></div>"
    )
    HTML_TAG_STATUS_ACTIVE_COLOR = (
        "<div class='center-block' style='background-color:"
        + settings.STATUS_ACTIVE_COLOR
        + ";color:#FFFFFF;width:100px;text-align: center;'><b> Active <b></div>"
    )


    organization_id = models.AutoField(SINGULAR_TITLE + " Id", primary_key=True)
    organization_name = models.CharField(
        "Name", max_length=191, blank=False, unique=True, default=None
    )
    organization_email = models.EmailField("Email", max_length=100,default="")
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+250123456789'. Up to 15 digits allowed.",
    )
    organization_phone_number = models.CharField("Phone Number",
        validators=[phone_regex, MinLengthValidator(10), MaxLengthValidator(15)],
        max_length=13,
        blank=True,
    )
    organization_type = models.CharField("Type", max_length=191, default="")
    organization_sub_type = models.CharField("Sub Type", max_length=191, default="")
    organization_category = models.CharField("Category", max_length=191, default="")
    organization_financial_agent_class = models.CharField("Financial Agency class", max_length=250, default="")
    organization_financial_agent_sub_class = models.CharField("Financial Agency Sub class", max_length=250, default="")
    organization_financial_schemes_name = models.CharField("Financial schemes Name", max_length=250, default="")
    organization_financial_schemes_class = models.CharField("Financial schemes class", max_length=250, default="")
    organization_financial_schemes_sub_class = models.CharField("Financial schemes Sub class", max_length=250, default="")
    organization_financial_sources_class = models.CharField("Financial Sources class", max_length=250, default="")
    organization_financial_sources_sub_class = models.CharField("Financial Sources Sub class", max_length=250, default="")
    organization_healthcare_class = models.CharField("HealthCare Provider Class", max_length=250, default="")
    organization_healthcare_sub_class = models.CharField("HealthCare Provider Sub Class", max_length=250, default="")
    organization_created_at = models.IntegerField("Created At", blank=False, default=0)
    organization_created_by = models.IntegerField("Created By", blank=False, default=0)
    organization_updated_at = models.IntegerField("Updated At", blank=False, default=0)
    organization_updated_by = models.IntegerField("Updated By", blank=False, default=0)
    organization_status = models.IntegerField(
        "Status", blank=False, default=STATUS_INNACTIVE
    )

    def __unicode__(self):
        return self.organization_id
