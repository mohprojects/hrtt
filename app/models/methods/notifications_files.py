from app import settings
from app.models.files import Files
from app.models.methods.emails import send_email
from app.models.methods.notifications import Methods_Notifications
from app.models.methods.sms import Methods_Sms
from app.models.users import Users


class Methods_Notifications_Files:
    @classmethod
    async def notify(cls, user: Users, item: Users, file: Files, subject, message):
        print(item.user_username)
        try:
            await Methods_Notifications.add(
                user,
                item,
                Methods_Notifications.TYPE_NONE,
                settings.MODEL_FILES,
                file.file_id,
                message,
            )
        except Exception as e:
            print(str(e))
        try:
            send_email(
                user.user_id,
                user.user_username,
                item.user_username,
                item.user_name,
                Methods_Notifications.TYPE_NONE,
                settings.MODEL_FILES,
                file.file_id,
                subject,
                message,
            )
        except Exception as e:
            print(str(e))
        try:
            await Methods_Sms.send_notification(
                user,
                item.user_contact_phone_number,
                Methods_Notifications.TYPE_NONE,
                settings.MODEL_FILES,
                file.file_id,
                message,
            )
        except Exception as e:
            print(str(e))
