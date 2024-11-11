from app import settings


class Methods_Status:

    TEXT_STATUS_DRAFT = "Draft"
    TEXT_STATUS_SUBMITTED = "Submitted"
    TEXT_STATUS_ACCEPTED = "Accepted"
    TEXT_STATUS_REJECTED = "Rejected"
    TEXT_STATUS_ACTIVE = "Active"
    TEXT_STATUS_BLOCKED = "Blocked"
    TEXT_STATUS_INACTIVE = "Inactive"

    STATUS_DRAFT = 0
    STATUS_SUBMITTED = 1
    STATUS_ACCEPTED = 2
    STATUS_REJECTED = 3
    STATUS_ACTIVE = 4
    STATUS_BLOCKED = 5
    STATUS_INACTIVE = 6

    ARRAY_STATUS = [
        STATUS_DRAFT,
        STATUS_SUBMITTED,
        STATUS_ACCEPTED,
        STATUS_REJECTED,
        STATUS_ACTIVE,
        STATUS_BLOCKED,
        STATUS_INACTIVE
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_DRAFT,
        TEXT_STATUS_SUBMITTED,
        TEXT_STATUS_ACCEPTED,
        TEXT_STATUS_REJECTED,
        TEXT_STATUS_ACTIVE,
        TEXT_STATUS_BLOCKED,
        TEXT_STATUS_INACTIVE
    ]
    DROPDOWN_STATUS = (
        ("", "--select--"),
        (STATUS_DRAFT, TEXT_STATUS_DRAFT),
        (STATUS_SUBMITTED, TEXT_STATUS_SUBMITTED),
        (STATUS_ACCEPTED, TEXT_STATUS_ACCEPTED),
        (STATUS_REJECTED, TEXT_STATUS_REJECTED),
        (STATUS_ACTIVE, TEXT_STATUS_ACTIVE),
        (STATUS_BLOCKED, TEXT_STATUS_BLOCKED),
        (STATUS_INACTIVE,TEXT_STATUS_INACTIVE),
    )
    
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
