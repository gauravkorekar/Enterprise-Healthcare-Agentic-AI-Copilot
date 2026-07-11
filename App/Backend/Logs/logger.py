import os
import logging

LOG_DIR = "Backend/Logs"
LOG_FILE = os.path.join(LOG_DIR, "mediassist.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("mediassist")

if not logger.handlers:

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)