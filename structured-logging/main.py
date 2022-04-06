from datetime import datetime
import json
import logging
import traceback
import sys

APP_NAME = 'structured-logging'
APP_VERSION = 'effda69c518a352371848690b3676738747ef776'
LOG_LEVEL = logging._nameToLevel['INFO']

class JsonEncoderStrFallback(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError as exc:
            if 'not JSON serializable' in str(exc):
                return str(obj)
            raise

class JsonEncoderDatetime(JsonEncoderStrFallback):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S%z')
        else:
            return super().default(obj)

logging.basicConfig(
    format='%(json_formatted)s',
    level=LOG_LEVEL,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("structured-logging.log")
    ]
)

_record_factory_bak = logging.getLogRecordFactory()
def record_factory(*args, **kwargs) -> logging.LogRecord:
    record = _record_factory_bak(*args, **kwargs)

    record.json_formatted = json.dumps(
    {
      'level': record.levelname,
      'unixtime': record.created,
      'thread': record.thread,
      'location': '{}:{}:{}'.format(
        record.pathname or record.filename,
        record.funcName,
        record.lineno,
      ),
      'exception': record.exc_info,
      'traceback': traceback.format_exception(*record.exc_info) if record.exc_info else None,
      'app': {
        'name': APP_NAME,
        'releaseId': APP_VERSION,
        'message': record.getMessage(),
      },
    },
        cls=JsonEncoderDatetime,
    )

    return record

logging.setLogRecordFactory(record_factory)

logging.info("Hello World")