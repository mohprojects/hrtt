from app import settings
from app.models.reports import Reports
from app.models.methods.emails import send_email
from app.models.methods.notifications import Methods_Notifications


class Methods_Notifications_Reports:
    @classmethod
    async def notify(
        cls, user, usersModel, item, itemModel, report: Reports, subject, message
    ):
        userId = 0
        userName = None
        userEmail = None
        if usersModel == "users":
            userId = user.user_id
            userName = user.user_name
            userEmail = user.user_username
      
        itemId = 0
        itemName = None
        itemEmail = None
        if itemModel == "users":
            itemId = item.user_id
            itemName = item.user_name
            itemEmail = item.user_username

        try:
            await Methods_Notifications.add(
                userId,
                userName,
                usersModel,
                itemId,
                itemName,
                itemModel,
                Methods_Notifications.TYPE_NONE,
                settings.MODEL_REPORTS,
                report.report_id,
                message,
            )
        except Exception:
            pass
        # try:
        #     send_email(
        #         userId,
        #         userEmail,
        #         itemEmail,
        #         itemName,
        #         Methods_Notifications.TYPE_NONE,
        #         settings.MODEL_REPORTS,
        #         report.report_id,
        #         subject,
        #         message,
        #     )
        # except Exception:
        #     pass
        # try:
        #     await Methods_Sms.send_notification(
        #         user,
        #         item.user_contact_phone_number,
        #         Methods_Notifications.TYPE_NONE,
        #         settings.MODEL_REPORTS,
        #         report.report_id,
        #         message
        #     )
        # except Exception as e:
        #     pass
