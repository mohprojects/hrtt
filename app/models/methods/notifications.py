from asyncio.log import logger

from app import settings
from app.models.methods.mongo import Methods_Mongo
from app.models.users import Users
from app.utils import Utils


class Methods_Notifications:

    TYPE_NONE = 0
    STATUS_READ = 1
    STATUS_UNREAD = 0

    @classmethod
    async def add(
        cls,
        userFr,
        userFrName,
        userFrModel,
        userTo,
        userToName,
        userToModel,
        type,
        model,
        modelId,
        message,
    ):
        doc_log = {}
        doc_log["fr"] = userFr
        doc_log["frModel"] = userFrModel
        doc_log["to"] = userTo
        doc_log["toModel"] = userToModel
        doc_log["type"] = type
        doc_log["model"] = model
        doc_log["modelId"] = modelId
        doc_log["message"] = message
        doc_log["updatedAt"] = Utils.get_current_datetime_utc()
        doc_log["updatedBy"] = userFrName
        doc_log["readAt"] = None
        doc_log["readStatus"] = Methods_Notifications.STATUS_UNREAD

        try:
            col_log = Methods_Mongo.get_collection(settings.MODEL_NOTIFICATIONS)
            col_log.insert_one(doc_log)
        except Exception as e:
            err = "Notifications insert not working. Error: " + str(e)
            print(err)
            logger.error(err)
            

        return col_log



# class Methods_Notifications:

#     TYPE_NONE = 0

#     STATUS_READ = 1
#     STATUS_UNREAD = 0

#     @classmethod
#     async def add(cls, userFr, userTo, type, model, modelId, message):
       
#         print(f"***************************** from: {userFr} To: {userTo} Type :{type} Model: {model} model_id: {modelId} message: {message}")
#         doc_log = {}
#         doc_log["fr"] = userFr.user_id
#         doc_log["to"] = userTo.user_id
#         doc_log["type"] = type
#         doc_log["model"] = model
#         doc_log["modelId"] = modelId
#         doc_log["message"] = message
#         doc_log["updatedAt"] = Utils.get_current_datetime_utc()
#         doc_log["updatedBy"] = userFr.user_name
#         doc_log["readAt"] = None
#         doc_log["readStatus"] = Methods_Notifications.STATUS_UNREAD

#         try:
#             col_log = Methods_Mongo.get_collection(settings.MODEL_NOTIFICATIONS)
#             col_log.insert_one(doc_log)
#         except Exception as e:
#             err = "Notifications insert not working. Error: " + str(e)
#             print(err)
#             logger.error(err)

#         return col_log
