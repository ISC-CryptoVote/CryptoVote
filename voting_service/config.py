import os
import logging
import sys

FORMAT = "%(asctime)s - (%(name)s) - %(levelname)s - %(message)s"

logging.basicConfig(format=FORMAT)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
for handler in logger.handlers:
    logger.removeHandler(handler)

logger.addHandler(handler)

DEBUG_MODE = os.getenv("DEBUG_MODE", False)

MASTER_HOST = os.getenv('MASTER_HOST', '0.0.0.0')

MASTER_PORT = os.getenv('MASTER_PORT', 8000)

DB_HOST = os.getenv('DB_HOST', 'localhost')

DB_PORT = os.getenv('DB_PORT', 8001)