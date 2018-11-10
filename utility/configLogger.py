from datetime import datetime


def currentTimestampLogger():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')#("%S-%M-%H-%d-%m-%Y")

APPLICATION_NAME = "Piternet"
DESTINATION = "log/"

def configLogger(name=None):
    if name:
        name += "-"+APPLICATION_NAME
    else:
        name = APPLICATION_NAME
    destination = ""
    if DESTINATION:
        destination = DESTINATION
    return {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s|[%(levelname)s]|%(name)s|%(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },

        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": destination+currentTimestampLogger()+".log", #destination + name+" - info - "+currentTimestampLogger()+".log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        },

        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "simple",
            "filename": destination+currentTimestampLogger()+".log", #destination + name+" - errors - "+currentTimestampLogger()+".log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },

    "loggers": {
        "my_module": {
            "level": "DEBUG", #"ERROR", #"DEBUG",
            "handlers": ["console"],
            "propagate": "no"
        }
    },

    "root": {
        "level": "DEBUG", #"INFO", #"DEBUG",
        "handlers": ["console", "info_file_handler", "error_file_handler"]
    }
}

CONFIG_LOGGER = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },

        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": "info.log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        },

        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "simple",
            "filename": "errors.log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },

    "loggers": {
        "my_module": {
            "level": "ERROR", #"DEBUG",
            "handlers": ["console"],
            "propagate": "no"
        }
    },

    "root": {
        "level": "INFO", #"DEBUG",
        "handlers": ["console", "info_file_handler", "error_file_handler"]
    }
}

RUN_APP = 1
TEST_AMBIENT = 0
AMBIENT = RUN_APP
