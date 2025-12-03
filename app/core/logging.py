import logging
import sys
from app.core.config import settings

def setup_logging():
    """
    Configures the logging for the application.
    """
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Avoid adding multiple handlers if they already exist
    if not logger.handlers:
        logger.addHandler(console_handler)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    return logger

logger = setup_logging()
