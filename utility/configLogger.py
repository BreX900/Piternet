from datetime import datetime

from utility.system import System, system


def currentTimestampLogger():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def configLogger(name: str, destination: str = "log/", dt: datetime=None):
    if dt is None:
        dt = datetime.now()
    dt: str = dt.strftime("%Y-%m-%d-%H-%M-%S")
    destination += str(dt)+"/"
    import os
    if not os.path.exists(destination):
        os.makedirs(destination)
    isWindows = system == System.WINDOWS
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "-%(asctime)s -%(name)s -%(levelname)s -%(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": ("DEBUG" if isWindows else "ERROR"),
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": destination + name + " - info - " + dt + ".log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            },

            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": destination + name + " - errors - " + dt + ".log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            }
        },

        "loggers": {
            "my_module": {
                "level": ("DEBUG" if isWindows else "ERROR"),
                "handlers": ["console"],
                "propagate": "no"
            }
        },

        "root": {
            "level": ("DEBUG" if isWindows else "INFO"),
            "handlers": ["console", "info_file_handler", "error_file_handler"]
        }
    }