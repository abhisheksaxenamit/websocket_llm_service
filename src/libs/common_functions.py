from argparse import Namespace
import json
from libs.logger_config import logger

def load_config_from_json(config_path: str) -> Namespace:
    """Load configuration from a JSON file and return as Namespace."""
    try:
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)
        return Namespace(**config_data)
    except FileNotFoundError:
        print("Configuration file not found")
        logger.error(f"Configuration file not found at {config_path}")
        return Namespace()
    except json.JSONDecodeError:
        print("Error decoding JSON from the configuration file")
        logger.error(f"Error decoding JSON from the configuration file at {config_path}")
        return Namespace()

def log_message(origin: str, message: str, level: str = 'info') -> None:
    """Log a message at the specified logging level."""
    if level == 'debug':
        logger.debug(f"{origin}: {message}")
    elif level == 'warning':
        logger.warning(f"{origin}: {message}")
    elif level == 'error':
        logger.error(f"{origin}: {message}")
    else:
        logger.info(f"{origin}: {message}")