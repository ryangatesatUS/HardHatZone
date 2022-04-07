from datetime import datetime
import json
import logging
import traceback
import sys
import socket

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
        'uslog': {
            'timestamp': record.created,
            'hostname': socket.gethostname(),
            'service_id': APP_NAME,
            'service_version': APP_VERSION,
            'service_commit_hash': 'tbd',
            'log_version': '1.0.1',
            'log_level': record.levelname,
            'logger_name': record.funcName,
            'log_type': 'logs',
            'security_context': '',
            'exception': record.exc_info,
            'trace': traceback.format_exception(*record.exc_info) if record.exc_info else None,
            
            'thread': record.thread,
            'message': record.getMessage(),
            'location': '{}:{}:{}'.format(
                record.pathname or record.filename,
                record.funcName,
                record.lineno,
            )
        }
    },
        cls=JsonEncoderDatetime,
    )

    return record

logging.setLogRecordFactory(record_factory)

logging.info("Hello World")