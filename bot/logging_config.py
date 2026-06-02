import logging
import os


def setup_logger() -> logging.Logger:
    """
    Configure the TradingBot logger.

    - DEBUG and above → logs/bot_activity.log  (full detail for audit trail)
    - WARNING and above → stderr console       (surface issues to the operator)
    """
    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("TradingBot")

    # Guard: don't add handlers more than once (e.g. on repeated imports)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # ── File handler (DEBUG+) ────────────────────────────────────────────────
    file_handler = logging.FileHandler("logs/bot_activity.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    # ── Console handler (WARNING+) ───────────────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(
        logging.Formatter("%(levelname)s: %(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()
