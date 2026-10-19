# src/logger.py
import logging
from pathlib import Path

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:          # avoid duplicate handlers
        return logger
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )
    Path("logs").mkdir(exist_ok=True)

    file_handler = logging.FileHandler("logs/pipeline.log")
    file_handler.setFormatter(fmt)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

#FileHandler → writes everything to a file (logs/pipeline.log), including DEBUG
##StreamHandler → prints to the console (stderr by default), filtered to INFO and above
