import sys

from loguru import logger

# For scripts
config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", "backtrace": True,
         "diagnose": True},
        # {"sink": "file.log", "serialize": True},
    ],
    "extra": {"user": "someone"}
}
logger.configure(**config)

# For libraries
logger.disable("my_library")
logger.info("No matter added sinks, this message is not displayed")
logger.enable("my_library")
logger.info("This message however is propagated to the sinks")

def func(a, b):
    return a / b

def nested(c):
    try:
        func(5, c)
    except ZeroDivisionError:
        logger.exception("What?!")

nested(0)