from asyncio.log import logger
from app import settings
from app.models.methods.mongo import Methods_Mongo
from app.utils import Utils


class Methods_Logs:
    @classmethod
    async def add(cls, model, modelId, message, updatedId, updatedBy):
        doc_log = {}
        doc_log["model"] = model
        doc_log["modelId"] = modelId
        doc_log["message"] = message
        doc_log["updatedAt"] = Utils.get_current_datetime_utc()
        doc_log["updatedId"] = updatedId
        doc_log["updatedBy"] = updatedBy

        try:
            col_log = Methods_Mongo.get_collection(settings.MODEL_LOGS)
            col_log.insert_one(doc_log)
        except Exception as e:
            err = "Logs insert not working. Error: " + str(e)
            print(err)
            logger.error(err)

        return col_log

    @classmethod
    def data(cls, model):
        col_log = Methods_Mongo.get_collection(settings.MODEL_LOGS)
        logs = col_log.find({})
        return logs
