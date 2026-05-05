#!/usr/bin/env python3

import logging
import os
from pathlib import Path

LOG_DIR = Path(os.getenv("LOG_DIR", "/work/logs"))

# --- ANSI colors ---
RESET = "\033[0m"
WHITE = "\033[37m"
YELLOW = "\033[33m"
RED = "\033[31m"

LEVEL_COLORS = {
    "INFO": WHITE,
    "WARNING": YELLOW,
    "ERROR": RED,
    "CRITICAL": RED,
}


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt, use_colors=True):
        super().__init__(fmt)
        self.use_colors = use_colors

    def format(self, record):
        if self.use_colors:
            color = LEVEL_COLORS.get(record.levelname, RESET)
            record.levelname = f"{color}{record.levelname}{RESET}"
        return super().format(record)


def setup_logger(name="runner"):
    logger = logging.getLogger(name)

    # Log level via env, default INFO
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(log_level)

    if logger.handlers:
        return logger

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # --- File handler (no colors, timestamped) ---
    file_handler = logging.FileHandler(LOG_DIR / "runner.log")
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # --- Console handler ---
    use_colors = os.getenv("LOG_COLORS", "true").lower() == "true"
    console_handler = logging.StreamHandler()
    console_formatter = ColorFormatter(
        "[%(levelname)s] %(message)s",
        use_colors=use_colors
    )
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
