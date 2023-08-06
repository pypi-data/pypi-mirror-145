""" module:: dlt.adapter
    :synopsis: The adapter linking the dlt stream into the python logging mechanism.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""

import logging

from dlt.protocol import DltLogLevel, DltRecordType
from dlt.serial_port import SerialStreamHandler

LOG_LEVEL_MAPPING = {DltLogLevel.FATAL: logging.FATAL,
                     DltLogLevel.ERROR: logging.ERROR,
                     DltLogLevel.WARN: logging.WARNING,
                     DltLogLevel.INFO: logging.INFO,
                     DltLogLevel.DEBUG: logging.DEBUG,
                     DltLogLevel.VERBOSE: logging.NOTSET}


class DltAdapter(SerialStreamHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, record):
        if record.get("record_type") == DltRecordType.LOG:
            name = "dlt"
            level = LOG_LEVEL_MAPPING.get(record.get("log_level"))
            if level is None:
                level = logging.DEBUG
            msg = record.get("payload_text")
            if msg is not None:
                keys_for_extra = ["sessionid", "ecuid", "timestamp", "applicationid", "contextid", ]
                extra = {val: key for val, key in record.items() if key in keys_for_extra}
                logger = logging.getLogger(name=name)
                logger.log(level=level, msg=msg, extra=extra)
