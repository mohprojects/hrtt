# from django.conf import settings
from app import settings


def global_settings(request):
    # return any necessary values
    return {
        # Project related
        'TEMPLATE_PATH_BACKEND': settings.TEMPLATE_PATH_BACKEND,
        'TEMPLATE_PATH_FRONTEND': settings.TEMPLATE_PATH_FRONTEND,


        # SYSTEM
        "IS_LOCAL": settings.IS_LOCAL,
        # Captcha
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        # # Files
        "APP_FILES_URL": settings.APP_FILES_URL,
        "APP_FILES_URL_LOCAL": settings.APP_FILES_URL_LOCAL,
        "APP_FILES_XAUTH": settings.APP_FILES_XAUTH,
        # # Office
        "APP_OFFICE_URL": settings.APP_OFFICE_URL,
        "APP_OFFICE_URL_LOCAL": settings.APP_OFFICE_URL_LOCAL,
        "APP_OFFICE_XAUTH": settings.APP_OFFICE_XAUTH,
        # Project related
        "APP_CONSTANT_COMPANY": settings.APP_CONSTANT_COMPANY,
        "APP_CONSTANT_APP_NAME": settings.APP_CONSTANT_APP_NAME,
        "APP_CONSTANT_APP_SHORT_NAME": settings.APP_CONSTANT_APP_SHORT_NAME,
        "APP_CONSTANT_APP_NAME_NO_SPACE": settings.APP_CONSTANT_APP_NAME_NO_SPACE,
        "APP_CONSTANT_APP_PACKAGE_NAME": settings.APP_CONSTANT_APP_PACKAGE_NAME,
        "APP_CONSTANT_APP_VERSION_CODE": settings.APP_CONSTANT_APP_VERSION_CODE,
        "APP_CONSTANT_APP_VERSION_NAME": settings.APP_CONSTANT_APP_VERSION_NAME,
        "APP_CONSTANT_APP_VERSION_MOBILE": settings.APP_CONSTANT_APP_VERSION_MOBILE,
        "APP_CONSTANT_COMPANY_NAME": settings.APP_CONSTANT_COMPANY_NAME,
        "APP_CONSTANT_COMPANY_WEBSITE": settings.APP_CONSTANT_COMPANY_WEBSITE,
        "APP_CONSTANT_TECH_SUPPORT_EMAIL_ID": settings.APP_CONSTANT_TECH_SUPPORT_EMAIL_ID,
        "APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID": settings.APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID,
        # Datetime
        "TIME_ZONE": settings.TIME_ZONE,
        "APP_CONSTANT_DISPLAY_TIME_ZONE": settings.APP_CONSTANT_DISPLAY_TIME_ZONE,
        "APP_CONSTANT_DISPLAY_DATE_FORMAT": settings.APP_CONSTANT_DISPLAY_DATE_FORMAT,
        "APP_CONSTANT_DISPLAY_TIME_FORMAT": settings.APP_CONSTANT_DISPLAY_TIME_FORMAT,
        "APP_CONSTANT_DISPLAY_DATETIME_FORMAT": settings.APP_CONSTANT_DISPLAY_DATETIME_FORMAT,
        "APP_CONSTANT_INPUT_DATETIME_FORMAT": settings.APP_CONSTANT_INPUT_DATETIME_FORMAT,
        "APP_CONSTANT_INPUT_DATE_FORMAT": settings.APP_CONSTANT_INPUT_DATE_FORMAT,
        "APP_CONSTANT_INPUT_TIME_FORMAT": settings.APP_CONSTANT_INPUT_TIME_FORMAT,
        "APP_CONSTANT_DEFAULT_DATETIME": settings.APP_CONSTANT_DEFAULT_DATETIME,
        "APP_CONSTANT_DEFAULT_DATE": settings.APP_CONSTANT_DEFAULT_DATE,
        "APP_CONSTANT_DEFAULT_TIME": settings.APP_CONSTANT_DEFAULT_TIME,
        # Backend Sections
        "BACKEND_SECTION_DASHBOARD": settings.BACKEND_SECTION_DASHBOARD,
        "BACKEND_SECTION_USERS": settings.BACKEND_SECTION_USERS,
        "BACKEND_SECTION_PROFILE": settings.BACKEND_SECTION_PROFILE,
        "BACKEND_SECTION_CHANGE_PASSWORD": settings.BACKEND_SECTION_CHANGE_PASSWORD,
        "BACKEND_SECTION_SETTINGS": settings.BACKEND_SECTION_SETTINGS,
        "BACKEND_SECTION_HELP": settings.BACKEND_SECTION_HELP,
        "BACKEND_SECTION_LOGS": settings.BACKEND_SECTION_LOGS,
        "BACKEND_SECTION_FILES": settings.BACKEND_SECTION_FILES,
        "BACKEND_SECTION_NOTIFICATIONS": settings.BACKEND_SECTION_NOTIFICATIONS,
        "BACKEND_SECTION_ORGANIZATIONS": settings.BACKEND_SECTION_ORGANIZATIONS,
        "BACKEND_SECTION_ORGANIZATION": settings.BACKEND_SECTION_ORGANIZATION,
        "BACKEND_SECTION_ANALYSIS": settings.BACKEND_SECTION_ANALYSIS,
        # "BACKEND_SECTION_DIVISIONS": settings.BACKEND_SECTION_DIVISIONS,
        "BACKEND_SECTION_PROJECTS": settings.BACKEND_SECTION_PROJECTS,
        "BACKEND_SECTION_ACTIVITIES": settings.BACKEND_SECTION_ACTIVITIES,
        "BACKEND_SECTION_LEVELS": settings.BACKEND_SECTION_LEVELS,
        'BACKEND_SECTION_REPORTERS': settings.BACKEND_SECTION_REPORTERS,
        'BACKEND_SECTION_REPORTS': settings.BACKEND_SECTION_REPORTS,
        'BACKEND_SECTION_CURRENCY_RATES': settings.BACKEND_SECTION_CURRENCY_RATES,
        'BACKEND_SECTION_SYSTEM_REPORTS': settings.BACKEND_SECTION_SYSTEM_REPORTS,
        # User Permissions
        "ACCESS_PERMISSION_USER_CREATE": settings.ACCESS_PERMISSION_USER_CREATE,
        "ACCESS_PERMISSION_USER_UPDATE": settings.ACCESS_PERMISSION_USER_UPDATE,
        "ACCESS_PERMISSION_USER_DELETE": settings.ACCESS_PERMISSION_USER_DELETE,
        "ACCESS_PERMISSION_USER_VIEW": settings.ACCESS_PERMISSION_USER_VIEW,
        "ACCESS_PERMISSION_DASHBOARD_VIEW": settings.ACCESS_PERMISSION_DASHBOARD_VIEW,
        "ACCESS_PERMISSION_SETTINGS_VIEW": settings.ACCESS_PERMISSION_SETTINGS_VIEW,
        "ACCESS_PERMISSION_LOG_CREATE": settings.ACCESS_PERMISSION_LOG_CREATE,
        "ACCESS_PERMISSION_LOG_UPDATE": settings.ACCESS_PERMISSION_LOG_UPDATE,
        "ACCESS_PERMISSION_LOG_DELETE": settings.ACCESS_PERMISSION_LOG_DELETE,
        "ACCESS_PERMISSION_LOG_VIEW": settings.ACCESS_PERMISSION_LOG_VIEW,
        "ACCESS_PERMISSION_FILES_CREATE": settings.ACCESS_PERMISSION_FILES_CREATE,
        "ACCESS_PERMISSION_FILES_UPDATE": settings.ACCESS_PERMISSION_FILES_UPDATE,
        "ACCESS_PERMISSION_FILES_DELETE": settings.ACCESS_PERMISSION_FILES_DELETE,
        "ACCESS_PERMISSION_FILES_VIEW": settings.ACCESS_PERMISSION_FILES_VIEW,
        "ACCESS_PERMISSION_FILES_DOWNLOAD": settings.ACCESS_PERMISSION_FILES_DOWNLOAD,
        "ACCESS_PERMISSION_ORGANIZATIONS_CREATE": settings.ACCESS_PERMISSION_ORGANIZATIONS_CREATE,
        "ACCESS_PERMISSION_ORGANIZATIONS_UPDATE": settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE,
        "ACCESS_PERMISSION_ORGANIZATIONS_DELETE": settings.ACCESS_PERMISSION_ORGANIZATIONS_DELETE,
        "ACCESS_PERMISSION_ORGANIZATIONS_VIEW": settings.ACCESS_PERMISSION_ORGANIZATIONS_VIEW,
 
        "ACCESS_PERMISSION_PROJECTS_CREATE": settings.ACCESS_PERMISSION_PROJECTS_CREATE,
        "ACCESS_PERMISSION_PROJECTS_UPDATE": settings.ACCESS_PERMISSION_PROJECTS_UPDATE,
        "ACCESS_PERMISSION_PROJECTS_DELETE": settings.ACCESS_PERMISSION_PROJECTS_DELETE,
        "ACCESS_PERMISSION_PROJECTS_ASSIGN": settings.ACCESS_PERMISSION_PROJECTS_ASSIGN,
        "ACCESS_PERMISSION_PROJECTS_VIEW": settings.ACCESS_PERMISSION_PROJECTS_VIEW,
        "ACCESS_PERMISSION_ACTIVITIES_CREATE": settings.ACCESS_PERMISSION_ACTIVITIES_CREATE,
        "ACCESS_PERMISSION_ACTIVITIES_UPDATE": settings.ACCESS_PERMISSION_ACTIVITIES_UPDATE,
        "ACCESS_PERMISSION_ACTIVITIES_DELETE": settings.ACCESS_PERMISSION_ACTIVITIES_DELETE,
        "ACCESS_PERMISSION_ACTIVITIES_VIEW": settings.ACCESS_PERMISSION_ACTIVITIES_VIEW,
        "ACCESS_PERMISSION_ACTIVITIES_APPROVE": settings.ACCESS_PERMISSION_ACTIVITIES_APPROVE,
        "ACCESS_PERMISSION_ACTIVITIES_DENY": settings.ACCESS_PERMISSION_ACTIVITIES_DENY,
        'ACCESS_PERMISSION_ACTIVITIES_SUBMIT' :settings.ACCESS_PERMISSION_ACTIVITIES_SUBMIT,
        'ACCESS_PERMISSION_ACTIVITIES_ACCEPT' : settings.ACCESS_PERMISSION_ACTIVITIES_ACCEPT,
        'ACCESS_PERMISSION_ACTIVITIES_REJECT': settings.ACCESS_PERMISSION_ACTIVITIES_REJECT,

        "ACCESS_PERMISSION_COMMENTS_CREATE": settings.ACCESS_PERMISSION_COMMENTS_CREATE,
        "ACCESS_PERMISSION_COMMENTS_UPDATE": settings.ACCESS_PERMISSION_COMMENTS_UPDATE,
        "ACCESS_PERMISSION_COMMENTS_DELETE": settings.ACCESS_PERMISSION_COMMENTS_DELETE,
        "ACCESS_PERMISSION_COMMENTS_VIEW": settings.ACCESS_PERMISSION_COMMENTS_VIEW,
        
        "ACCESS_PERMISSION_REPORTS_CREATE": settings.ACCESS_PERMISSION_REPORTS_CREATE,
        "ACCESS_PERMISSION_REPORTS_UPDATE": settings.ACCESS_PERMISSION_REPORTS_UPDATE,
        "ACCESS_PERMISSION_REPORTS_DELETE": settings.ACCESS_PERMISSION_REPORTS_DELETE,
        "ACCESS_PERMISSION_REPORTS_VIEW": settings.ACCESS_PERMISSION_REPORTS_VIEW,
        "ACCESS_PERMISSION_REPORTS_SUBMIT": settings.ACCESS_PERMISSION_REPORTS_SUBMIT,
        "ACCESS_PERMISSION_REPORTS_ACCEPT": settings.ACCESS_PERMISSION_REPORTS_ACCEPT,
        "ACCESS_PERMISSION_REPORTS_REJECT": settings.ACCESS_PERMISSION_REPORTS_REJECT,
        
        "ACCESS_PERMISSION_REPORTS_APPROVE": settings.ACCESS_PERMISSION_REPORTS_APPROVE,
        "ACCESS_PERMISSION_REPORTS_DENY": settings.ACCESS_PERMISSION_REPORTS_DENY,
        "ACCESS_PERMISSION_LEVELS_CREATE": settings.ACCESS_PERMISSION_LEVELS_CREATE,
        "ACCESS_PERMISSION_LEVELS_UPDATE": settings.ACCESS_PERMISSION_LEVELS_UPDATE,
        "ACCESS_PERMISSION_LEVELS_DELETE": settings.ACCESS_PERMISSION_LEVELS_DELETE,
        "ACCESS_PERMISSION_LEVELS_VIEW": settings.ACCESS_PERMISSION_LEVELS_VIEW,

        "ACCESS_PERMISSION_CURRENCY_RATES_CREATE": settings.ACCESS_PERMISSION_CURRENCY_RATES_CREATE,
        "ACCESS_PERMISSION_CURRENCY_RATES_UPDATE": settings.ACCESS_PERMISSION_CURRENCY_RATES_UPDATE,
        "ACCESS_PERMISSION_CURRENCY_RATES_DELETE": settings.ACCESS_PERMISSION_CURRENCY_RATES_DELETE,
        "ACCESS_PERMISSION_CURRENCY_RATES_VIEW": settings.ACCESS_PERMISSION_CURRENCY_RATES_VIEW,
        "ACCESS_PERMISSION_SYSTEM_REPORTS_CREATE": settings.ACCESS_PERMISSION_SYSTEM_REPORTS_CREATE,
        "ACCESS_PERMISSION_SYSTEM_REPORTS_UPDATE": settings.ACCESS_PERMISSION_SYSTEM_REPORTS_UPDATE,
        "ACCESS_PERMISSION_SYSTEM_REPORTS_DELETE": settings.ACCESS_PERMISSION_SYSTEM_REPORTS_DELETE,
        "ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW": settings.ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW,
        # Model Titles
        "MODEL_USERS": settings.MODEL_USERS,
        "MODEL_USERS_PLURAL_TITLE": settings.MODEL_USERS_PLURAL_TITLE,
        "MODEL_USERS_SINGULAR_TITLE": settings.MODEL_USERS_SINGULAR_TITLE,
        "MODEL_LOGS": settings.MODEL_LOGS,
        "MODEL_LOGS_PLURAL_TITLE": settings.MODEL_LOGS_PLURAL_TITLE,
        "MODEL_LOGS_SINGULAR_TITLE": settings.MODEL_LOGS_SINGULAR_TITLE,
        "MODEL_FILES": settings.MODEL_FILES,
        "MODEL_FILES_PLURAL_TITLE": settings.MODEL_FILES_PLURAL_TITLE,
        "MODEL_FILES_SINGULAR_TITLE": settings.MODEL_FILES_SINGULAR_TITLE,
        "MODEL_NOTIFICATIONS": settings.MODEL_NOTIFICATIONS,
        "MODEL_NOTIFICATIONS_PLURAL_TITLE": settings.MODEL_NOTIFICATIONS_PLURAL_TITLE,
        "MODEL_NOTIFICATIONS_SINGULAR_TITLE": settings.MODEL_NOTIFICATIONS_SINGULAR_TITLE,
        "MODEL_SMS_LOGS": settings.MODEL_SMS_LOGS,
        "MODEL_SMS_LOGS_PLURAL_TITLE": settings.MODEL_SMS_LOGS_PLURAL_TITLE,
        "MODEL_SMS_LOGS_SINGULAR_TITLE": settings.MODEL_SMS_LOGS_SINGULAR_TITLE,
        "MODEL_EMAIL_LOGS": settings.MODEL_EMAIL_LOGS,
        "MODEL_EMAIL_LOGS_PLURAL_TITLE": settings.MODEL_EMAIL_LOGS_PLURAL_TITLE,
        "MODEL_EMAIL_LOGS_SINGULAR_TITLE": settings.MODEL_EMAIL_LOGS_SINGULAR_TITLE,
        "MODEL_ORGANIZATIONS": settings.MODEL_ORGANIZATIONS,
        "MODEL_ORGANIZATIONS_PLURAL_TITLE": settings.MODEL_ORGANIZATIONS_PLURAL_TITLE,
        "MODEL_ORGANIZATIONS_SINGULAR_TITLE": settings.MODEL_ORGANIZATIONS_SINGULAR_TITLE,
       
        "MODEL_PROJECTS": settings.MODEL_PROJECTS,
        "MODEL_PROJECTS_PLURAL_TITLE": settings.MODEL_PROJECTS_PLURAL_TITLE,
        "MODEL_PROJECTS_SINGULAR_TITLE": settings.MODEL_PROJECTS_SINGULAR_TITLE,
        
        "MODEL_ACTIVITIES": settings.MODEL_ACTIVITIES,
        "MODEL_ACTIVITIES_PLURAL_TITLE": settings.MODEL_ACTIVITIES_PLURAL_TITLE,
        "MODEL_ACTIVITIES_SINGULAR_TITLE": settings.MODEL_ACTIVITIES_SINGULAR_TITLE,
        
        "MODEL_ACTIVITIES_INPUTS": settings.MODEL_ACTIVITIES_INPUTS,
        "MODEL_ACTIVITIES_INPUTS_PLURAL_TITLE": settings.MODEL_ACTIVITIES_INPUTS_PLURAL_TITLE,
        "MODEL_ACTIVITIES_INPUTS_SINGULAR_TITLE": settings.MODEL_ACTIVITIES_INPUTS_SINGULAR_TITLE,
        
        "MODEL_LEVELS": settings.MODEL_LEVELS,
        "MODEL_LEVELS_PLURAL_TITLE": settings.MODEL_LEVELS_PLURAL_TITLE,
        "MODEL_LEVELS_SINGULAR_TITLE": settings.MODEL_LEVELS_SINGULAR_TITLE,
      
        'MODEL_FUNDINGS' : settings.MODEL_FUNDINGS,
        'MODEL_FUNDINGS_PLURAL_TITLE' : settings.MODEL_FUNDINGS_PLURAL_TITLE,
        'MODEL_FUNDINGS_SINGULAR_TITLE': settings.MODEL_FUNDINGS_SINGULAR_TITLE,
        
        'MODEL_REPORTS':settings.MODEL_REPORTS,
        'MODEL_REPORTS_PLURAL_TITLE': settings.MODEL_REPORTS_PLURAL_TITLE,
        'MODEL_REPORTS_SINGULAR_TITLE': settings.MODEL_REPORTS_SINGULAR_TITLE,

        'MODEL_CURRENCY_RATES':settings.MODEL_RATES,
        'MODEL_CURRENCY_RATES_PLURAL_TITLE': settings.MODEL_RATES_PLURAL_TITLE,
        'MODEL_CURRENCY_RATES_SINGULAR_TITLE': settings.MODEL_RATES_SINGULAR_TITLE,

        'MODEL_SYSTEM_REPORTS':settings.MODEL_SYSTEM_REPORTS,
        'MODEL_SYSTEM_REPORTS_PLURAL_TITLE': settings.MODEL_SYSTEM_REPORTS_PLURAL_TITLE,
        'MODEL_SYSTEM_REPORTS_SINGULAR_TITLE': settings.MODEL_SYSTEM_REPORTS_SINGULAR_TITLE,
        # Template Colors
        "COLOR_PRIMARY": settings.COLOR_PRIMARY,
        "COLOR_PRIMARY_DARK": settings.COLOR_PRIMARY_DARK,
        "COLOR_PRIMARY_LIGHT": settings.COLOR_PRIMARY_LIGHT,
        "COLOR_ACCENT": settings.COLOR_ACCENT,
    }
