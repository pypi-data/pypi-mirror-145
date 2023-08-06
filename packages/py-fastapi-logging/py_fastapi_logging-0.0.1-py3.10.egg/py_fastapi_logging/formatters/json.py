import datetime
import json
import logging
import traceback
from py_fastapi_logging.schemas.base import BaseJsonLogSchema


class JSONLogFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord, *args, **kwargs) -> str:
        log_object: dict = self._format_log_object(record)
        return json.dumps(log_object, ensure_ascii=False)

    @staticmethod
    def _format_log_object(record: logging.LogRecord) -> dict:
        now = datetime \
            .datetime \
            .fromtimestamp(record.created) \
            .astimezone() \
            .replace(microsecond=0) \
            .isoformat()

        json_log_fields = BaseJsonLogSchema(
            thread=record.process,
            timestamp=now,
            level=record.levelno,
            progname=record.progname,
            request_id=record.request_id
        )

        if record.exc_info:
            json_log_fields.exceptions = \
                traceback.format_exception(*record.exc_info)

        elif record.exc_text:
            json_log_fields.exceptions = record.exc_text

        json_log_object = json_log_fields.dict(
            exclude_unset=True,
            by_alias=True,
        )

        if hasattr(record, 'payload'):
            json_log_object["payload"] = record.payload


        return json_log_object
