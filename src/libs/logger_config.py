import logging
from time import strftime
import os
from pathlib import Path

date_time_format = strftime('%Y%m%d_%H%M%S')
file_path = Path(__file__).parent / 'logs' / f'{date_time_format}_app.log'
os.makedirs(file_path.parent, exist_ok=True)
logger = logging.getLogger('AppLogger')

logger.setLevel(logging.DEBUG)
# Prevent multiple handlers if the logger is configured multiple times
if not logger.handlers:
    # Create a file handler to log to a file
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.DEBUG)

    # Define log format
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add file handler to logger
    logger.addHandler(file_handler)