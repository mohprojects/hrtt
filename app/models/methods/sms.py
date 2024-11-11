from asyncio.log import logger
from app import settings
from app.models.methods.mongo import Methods_Mongo
from app.models.users import Users
from app.utils import Utils


class Methods_Sms:
    @classmethod
    async def send_notification(cls, user: Users, to, type, model, modelId, message):
        try:
            doc = {}
            doc["userId"] = user.user_id
            doc["type"] = type
            doc["model"] = model
            doc["modelId"] = modelId
            doc["smsTo"] = to
            doc["message"] = message
            doc["createdAt"] = Utils.get_current_datetime_utc()
            doc["updatedAt"] = Utils.get_current_datetime_utc()
            doc["attemptAt"] = None
            doc["attemptNo"] = 0
            doc["attemptResult"] = None
            try:
                col = Methods_Mongo.get_collection(settings.MODEL_SMS_LOGS)
                col.insert_one(doc)
            except Exception as e:
                err = "Sms logs insert not working. Error: " + str(e)
                print(err)
                logger.error(err)
        except Exception as err:
            err = "Sms send notification not working. Error: " + str(e)
            print(err)
            logger.error(err)
