from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models
from django.middleware.csrf import rotate_token
from django.utils.crypto import constant_time_compare, get_random_string, salted_hmac

from app import settings
from app.data import ARRAY_GENDER


class Users(models.Model):
    TITLE = settings.MODEL_USERS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_USERS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())
    DEFAULT_PASSWORD = "Hrtt@123"

    SESSION_KEY = "_" + TITLE.lower() + "_id"
    SESSION_MASTER_KEY = "_" + TITLE.lower() + "_"
    HASH_SESSION_KEY = "_" + TITLE.lower() + "_hash"
    REDIRECT_FIELD_NAME = "next"

    ADMIN_DEFAULT_PERMISSIONS_LIST =[
    'activities-approve',
    'activities-create',
    'activities-delete',
    'activities-deny',
    'activities-update',
    'activities-view',
    'capital-formation-approve',
    'capital-formation-create',
    'capital-formation-delete',
    'capital-formation-deny',
    'capital-formation-update',
    'capital-formation-view', 
    'comments-create',
    'comments-delete',
    'comments-update',
    'comments-view',
    'currency-rate-create',
    'currency-rate-delete',
    'currency-rate-update',
    'currency-rate-view',
    'dashboard-view',
    'levels-create',
    'levels-delete',
    'levels-update',
    'levels-view',
    'log-create',
    'log-delete',
    'log-update',
    'log-view',
    'organizations-create',
    'organizations-delete',
    'organizations-update',
    'organizations-view',
    'projects-create',
    'projects-delete',
    'projects-update',
    'projects-view',
    'settings-view',
    'system-reports-create',
    'system-reports-delete',
    'system-reports-update',
    'system-reports-view',
    'user-create',
    'user-delete',
    'user-update',
    'user-view'

    ]

    ACTIVITY_MANAGER_DEFAULT_PERMISSIONS_LIST = [
        "activities-create",
        "activities-delete",
        "activities-update",
        "activities-accept",
        "activities-reject",
        "activities-submit",
        "activities-view",
        "capital-formation-create",
        "capital-formation-delete",
        "capital-formation-update",
        "capital-formation-accept",
        "capital-formation-reject",
        "capital-formation-submit",
        "capital-formation-view",
        "comments-create",
        "comments-update",
        "comments-view",
        "dashboard-view",
        "levels-view",
        "log-create",
        "log-delete",
        "log-update",
        "log-view",
        "organizations-update",
        "organizations-view",
        "projects-assign",
        "projects-create",
        "projects-delete",
        "projects-update",
        "projects-view",
        "settings-view",
        "user-create",
        "user-delete",
        "user-update",
        "user-view",   
    ]

    DATA_REPORTERS_DEFAULT_PERMISSIONS_LIST = [
        "activities-create",
        "activities-delete",
        "activities-submit",
        "activities-update",
        "activities-view",
        "capital-formation-create",
        "capital-formation-delete",
        "capital-formation-update",
        "capital-formation-submit",
        "capital-formation-view",
        "comments-view",
        "dashboard-view",
        "projects-view",
    ]
    
    # ROLES 
    TYPE_SUPER_ADMIN = "super-admin"
    TYPE_ACTIVITY_MANAGER = "activity-manager"
    TYPE_DATA_REPORTER = "data-reporter"
    TYPE_OTHER = "other"
    
    DROPDOWN_TYPE = [
        TYPE_SUPER_ADMIN.replace("-", " ").title(),
        TYPE_ACTIVITY_MANAGER.replace("-", " ").title(),
        TYPE_DATA_REPORTER.replace("-", " ").title()
        
    ]
    
    
    ROLE_NONE = "-"
    ARRAY_ROLES = (
        ("", "--select--"),
        (TYPE_SUPER_ADMIN, (TYPE_SUPER_ADMIN.title()).replace("-", " ")),
        (TYPE_ACTIVITY_MANAGER, (TYPE_ACTIVITY_MANAGER.title()).replace("-", " ")),
        (TYPE_DATA_REPORTER, (TYPE_DATA_REPORTER.title()).replace("-", " ")),
        #(TYPE_OTHER, (TYPE_OTHER.title()).replace("-", " ")),
    )
    
    # STATUS
    TEXT_STATUS_ACTIVE = "Logged in "
    TEXT_STATUS_INACTIVE = "Logged out"
    TEXT_STATUS_BLOCKED = "Blocked"
    TEXT_STATUS_UNVERIFIED = "Unverified"
    TEXT_STATUS_UNAPPROVED = "Unapproved"
    
    STATUS_ACTIVE = 0
    STATUS_INACTIVE = 1
    STATUS_BLOCKED = 2
    STATUS_UNVERIFIED = 3
    STATUS_UNAPPROVED = 4
    
    ARRAY_STATUS = [
        STATUS_ACTIVE,
        STATUS_INACTIVE,
        STATUS_BLOCKED,
        STATUS_UNVERIFIED,
        STATUS_UNAPPROVED,
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_ACTIVE,
        TEXT_STATUS_INACTIVE,
        TEXT_STATUS_BLOCKED,
        TEXT_STATUS_UNVERIFIED,
        TEXT_STATUS_UNAPPROVED,
    ]
      
    DROPDOWN_STATUS = (
        ("", "--select--"),
        (STATUS_ACTIVE, TEXT_STATUS_ACTIVE),
        (STATUS_INACTIVE, TEXT_STATUS_INACTIVE),
        (STATUS_BLOCKED, TEXT_STATUS_BLOCKED),
        (STATUS_UNVERIFIED, TEXT_STATUS_UNVERIFIED),
        (STATUS_UNAPPROVED, TEXT_STATUS_UNAPPROVED),
    )
    
    HTML_TAG_STATUS_ACTIVE_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_ACTIVE_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Logged in <b></div>'
    HTML_TAG_STATUS_INACTIVE_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_INACTIVE_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Logged out <b></div>'
    HTML_TAG_STATUS_BLOCKED_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_BLOCKED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Blocked <b></div>'
    HTML_TAG_STATUS_UNVERIFIED_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_UNVERIFIED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Unverified <b></div>'
    HTML_TAG_STATUS_UNAPPROVED_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_UNAPPROVED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Unapproved <b></div>'



    user_id = models.AutoField(SINGULAR_TITLE + " Id", primary_key=True)
    user_type = models.CharField(
        "Type", max_length=20, blank=False, choices=ARRAY_ROLES, default=TYPE_OTHER
    )
    user_username = models.CharField(
        "Username", max_length=100, blank=False, unique=True
    )
    user_auth_key = models.CharField("Auth key", max_length=255, blank=False)
    user_password_hash = models.CharField("Password", max_length=255, blank=False)
    user_password_reset_token = models.CharField(
        "Password reset token", max_length=255, blank=True
    )

    user_name = models.CharField('Name', max_length=100, blank=False)
    user_first_name = models.CharField("First Name", max_length=50, blank=False, default='')
    user_middle_name = models.CharField("Middle Name", max_length=50, blank=False, default='')
    user_last_name = models.CharField("Last Name", max_length=50, blank=False, default='')
    user_gender = models.CharField(
        "Gender", max_length=6, choices=ARRAY_GENDER, default=""
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+250123456789'. Up to 15 digits allowed.",
    )
    user_contact_phone_number = models.CharField(
        "Phone Number",
        validators=[phone_regex, MinLengthValidator(10), MaxLengthValidator(15)],
        max_length=15,
        blank=True,
    )
    user_contact_email_id = models.EmailField("Email id", max_length=100, blank=True)
    user_profile_photo_file_path = models.CharField(
        "Profile photo file path", max_length=255, blank=True
    )

    user_role = models.CharField(
        'Role', max_length=255, blank=True)
    organization_id = models.IntegerField('Organization', blank=False, default=0)
    user_created_at = models.IntegerField("Created At", blank=False, default=0)
    user_created_by = models.IntegerField("Created By", blank=False, default=0)
    user_updated_at = models.IntegerField("Updated At", blank=False, default=0)
    user_updated_by = models.IntegerField("Updated By", blank=False, default=0)
    user_status = models.IntegerField("Status", blank=False, default=STATUS_UNVERIFIED)

    def __unicode__(self):
        return self.user_id

    def get_session_auth_hash(self):
        key_salt = "hrtt.models.auth.Users.get_session_auth_hash"
        return salted_hmac(key_salt, self.user_password_hash).hexdigest()

    @classmethod
    def set_redirect_field_name(cls, request, url):
        request.session[Users.REDIRECT_FIELD_NAME] = url

    @classmethod
    def get_redirect_field_name(cls, request):
        return request.session.get(Users.REDIRECT_FIELD_NAME, None)

    @classmethod
    def get_session_key(cls, request):
        return str(request.session[Users.SESSION_KEY])

    @classmethod
    def login(cls, request, user):
        session_auth_hash = ""
        if hasattr(user, "get_session_auth_hash"):
            session_auth_hash = user.get_session_auth_hash()

        if Users.SESSION_KEY in request.session:
            if cls.get_session_key(request) != user.pk or (
                session_auth_hash
                and not constant_time_compare(
                    request.session.get(Users.HASH_SESSION_KEY, ""), session_auth_hash
                )
            ):
                request.session.flush()
        else:
            request.session.cycle_key()

        request.session[Users.SESSION_KEY] = str(user.pk)
        request.session[Users.SESSION_MASTER_KEY] = False
        request.session[Users.HASH_SESSION_KEY] = session_auth_hash
        # one hour session timeout
        request.session.set_expiry(3600)
        # reset csrf token
        rotate_token(request)
        return True

    @classmethod
    def logout(cls, request):
        request.session.flush()
        return True

    @classmethod
    def login_required(cls, request):
        if Users.SESSION_KEY in request.session:
            user_id = request.session.get(Users.SESSION_KEY, "0")
            try:
                user = Users.objects.get(user_id=user_id)
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                user = None
            return user
        else:
            return None

    @classmethod
    def generate_unique_token(cls, users, attribute):
        token = ""
        unique_token_found = False
        while not unique_token_found:
            token = get_random_string(32)
            if users.objects.filter(**{attribute: token}).count() == 0:
                unique_token_found = True
        return token

    @classmethod
    def generate_random_number(cls, attribute, length):
        token = ""
        unique_token_found = False
        while not unique_token_found:
            token = get_random_string(length, allowed_chars="0123456789")
            if (not token.startswith("0")) and Users.objects.filter(
                **{attribute: token}
            ).count() == 0:
                unique_token_found = True
        return token
