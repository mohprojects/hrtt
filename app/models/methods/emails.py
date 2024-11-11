from asyncio.log import logger
import json
import requests
from threading import Thread

from app import settings
from app.utils import Utils
from django.template.loader import render_to_string


def send_email(
    userId,
    emailFr,
    emailTo,
    name,
    type,
    model,
    modelId,
    subject,
    message,
    html_content=None,
):
    try:
        if html_content is None:
            action_url = "{domain}/{path}".format(
                domain=Utils.get_backend_domain(), path=""
            )
            contact_url = settings.APP_CONSTANT_COMPANY_WEBSITE
            html_content = render_to_string(
                "email/email-info.html",
                {
                    "name": name,
                    "message": message,
                    "contact_url": contact_url,
                    "action_url": action_url,
                },

                
            )
        # obj = None
        doc = {}
        doc["userId"] = userId
        doc["type"] = type
        doc["model"] = model
        doc["modelId"] = modelId
        doc["emailFr"] = emailFr
        doc["emailTo"] = emailTo
        doc["emailCc"] = None
        doc["subject"] = subject
        doc["html"] = html_content
        doc["message"] = message
        doc["createdAt"] = Utils.get_current_datetime_utc()
        doc["updatedAt"] = Utils.get_current_datetime_utc()
        doc["attemptAt"] = Utils.get_current_datetime_utc()
        doc["attemptNo"] = 0
        doc["attemptResult"] = None
        url = settings.EMAIL_API
        payload = json.dumps(doc)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        
     
    except Exception as err:
        err = "Email send notification not working. Error: " + str(err)
        print(err)
        logger.error(err)


class Methods_Emails(Thread):
    @classmethod
    def send_verification_email(cls, request, to, name, role,organization_name, action_url):
        try:
            contact_url = settings.APP_CONSTANT_COMPANY_WEBSITE
            html_content = render_to_string(
                "email/email-confirmation.html",
                {
                    "name": name,
                    "role":role,
                    "organization_name":organization_name,
                    "contact_url": contact_url,
                    "confirm_url": action_url,
                },
            )

            send_email(
                0,
                settings.APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID,
                [to],
                name,
                0,
                "",
                0,
                settings.EMAIL_VERIFICATION_SUBJECT,
                settings.EMAIL_VERIFICATION_MESSAGE,
                html_content,
            )
            # result = send_mail(
            #     settings.EMAIL_VERIFICATION_SUBJECT,
            #     settings.EMAIL_VERIFICATION_MESSAGE,
            #     settings.APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID,
            #     [to],
            #     fail_silently=False,
            #     html_message=html_content,
            # )
            # print(result)
        except Exception as err:
            print(err)
            logger.error(err)
        return True

    @classmethod
    def send_reset_password_email(cls, request, to, name, action_url):
        try:
            contact_url = settings.APP_CONSTANT_COMPANY_WEBSITE
            html_content = render_to_string(
                "email/email-reset-password.html",
                {
                    "name": name,
                    "contact_url": contact_url,
                    "reset_url": action_url,
                },
            )
            send_email(
                0,
                settings.APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID,
                [to],
                name,
                0,
                "",
                0,
                settings.EMAIL_PASSWORD_RESET_SUBJECT,
                settings.EMAIL_PASSWORD_RESET_MESSAGE,
                html_content,
            )
            # result = send_mail(
            #     settings.EMAIL_PASSWORD_RESET_SUBJECT,
            #     settings.EMAIL_PASSWORD_RESET_MESSAGE,
            #     settings.APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID,
            #     [to],
            #     fail_silently=False,
            #     html_message=html_content,
            # )
            # print('email response')
            # print(result)
        except Exception as err:
            logger.error(err)
        return True

    @classmethod
    def send_info_email(cls, request, to, name, message):
        try:
            contact_url = settings.APP_CONSTANT_COMPANY_WEBSITE
            html_content = render_to_string(
                "email/email-info.html",
                {
                    "name": name,
                    "message": message,
                    "contact_url": contact_url,
                },
            )
            send_email(
                0,
                settings.APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID,
                [to],
                name,
                0,
                "",
                0,
                settings.EMAIL_NOTIFICATION_SUBJECT,
                settings.EMAIL_NOTIFICATION_MESSAGE,
                html_content,
            )
            # result = send_mail(
            #     settings.EMAIL_NOTIFICATION_SUBJECT,
            #     settings.EMAIL_NOTIFICATION_MESSAGE,
            #     settings.APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID,
            #     [to],
            #     fail_silently=False,
            #     html_message=html_content,
            # )
            # print(result)
            return False, "Success"
        except Exception as err:
            print(err)
            logger.error(err)
            return True, str(err)
