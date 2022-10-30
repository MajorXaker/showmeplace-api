import inspect
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from pythonjsonlogger import jsonlogger
from dynaconf import Dynaconf

settings = Dynaconf(
    env="default",
    environments=True,
    default_settings_paths=["settings.toml", ".secrets.toml"],
    ROOT_PATH_FOR_DYNACONF=os.path.abspath(os.getcwd()),
)

LOG_FILENAME = "/tmp/python.log"

root = logging.getLogger()
for handler in list(root.handlers):
    root.removeHandler(handler)

log = logging.getLogger("smp-api")

log_level = logging.DEBUG if settings.LOGGING_LEVEL == "DEBUG" else logging.INFO
log.setLevel(log_level)


class ElkJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._skip_fields["color_message"] = "color_message"
        self._skip_fields.pop("pathname", None)

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["@timestamp"] = datetime.now().isoformat()
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["lineno"] = record.lineno
        log_record.update(self.get_extra_fields(record))

    def get_extra_fields(self, record):
        fields = {}

        frame = self.get_frame(record)
        if frame:
            cls = self.get_class(frame)
            if cls:
                fields["class_name"] = cls.__module__ + "." + cls.__name__

        return fields

    @staticmethod
    def get_frame(record: logging.LogRecord):
        frame = inspect.currentframe()
        while frame:
            frame = frame.f_back
            frameinfo = inspect.getframeinfo(frame)
            if frameinfo.filename == record.pathname:
                return frame

    @staticmethod
    def get_class(frame):
        if "self" in frame.f_locals:
            return type(frame.f_locals["self"])
        elif "cls" in frame.f_locals:
            return frame.f_locals["cls"]


if settings.JSON_LOGS:
    log_formatter = ElkJsonFormatter()
else:
    log_formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s] %(filename)s:%(lineno)d | %(message)s"
    )


if settings.LOG_TO_CONSOLE:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_formatter)

    root.addHandler(console_handler)


if settings.LOG_TO_FILE:
    file_handler = TimedRotatingFileHandler(
        LOG_FILENAME,
        when="D",
        interval=1,
        backupCount=30,
        encoding=None,
        delay=False,
        utc=True,
        atTime=None,
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)

    root.addHandler(file_handler)
