from argparse import Namespace
import json

def load_config_from_json(config_path: str) -> Namespace:
    """Load configuration from a JSON file and return as Namespace."""
    try:
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)
        return Namespace(**config_data)
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}")
        return Namespace()
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the configuration file at {config_path}")
        return Namespace()